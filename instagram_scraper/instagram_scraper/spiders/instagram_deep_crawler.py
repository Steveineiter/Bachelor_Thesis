# Selenium imports
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from parsel import Selector
import csv

# Other imports
import os
import wget
from scrapy import Spider
from scrapy.loader import ItemLoader
from instagram_scraper.items import PostDataItem, ProfileDataItem


from time import sleep
from instagram_scraper.constants import *


# TODO Ask: better one big file with many arguments, or 2 files with lots of duplicated code?
class InstagramSpider(Spider):
    name = "instagram_crawler"
    allowed_domains = ["instagram.com"]
    start_urls = ["http://instagram.com/"]

    def __init__(
        self,
        username=MARRYICETEA_INSTAGRAM_USERNAME,
        is_a_company: bool = True,
        is_a_deep_crawl=True,
        **kwargs,
    ):
        self.username = username
        self.is_a_company = is_a_company
        self.is_a_deep_crawl = is_a_deep_crawl
        # TODO Ask: it would be nicer with is_a_company.toUpper but on the other hand it needs more lines, what is better?
        #     Also it doesn't work with arguments :(
        if (
            is_a_company == "False"
            or is_a_company == "false"
            or is_a_company == "F"
            or is_a_company == "f"
            or is_a_company == "0"
        ):
            self.is_a_company = False
        if (
            is_a_deep_crawl == "False"
            or is_a_deep_crawl == "false"
            or is_a_deep_crawl == "F"
            or is_a_deep_crawl == "f"
            or is_a_deep_crawl == "0"
        ):
            self.is_a_deep_crawl = False

        super().__init__(**kwargs)

        working_directory = os.getcwd()
        webdriver_path = os.path.join(
            working_directory, os.pardir, os.pardir, "chromedriver"
        )
        # TODO Ugly AF, but again pycharm would complain otherwise...
        if self.is_a_company:
            self.csv_path = os.path.join(
                working_directory, os.pardir, COMPANY_PATH, username
            )
            self.image_path = os.path.join(
                working_directory, os.pardir, COMPANY_PATH, username, "images"
            )
        else:
            self.csv_path = os.path.join(
                working_directory, os.pardir, CONSUMER_PATH, username
            )
            self.image_path = os.path.join(
                working_directory, os.pardir, CONSUMER_PATH, username, "images"
            )

        # TODO Aks: Pycharm says i should not create it outside of init why? or is it w/e?
        # self.start_webdriver(working_directory)
        self.driver = webdriver.Chrome(webdriver_path)
        self.create_directory(self.csv_path)
        self.create_directory(self.image_path)

        self.profile_csv_file = open(
            os.path.join(self.csv_path, "profile_data.csv"), "w"
        )
        self.profile_writer = csv.writer(self.profile_csv_file)
        self.write_csv_header(self.profile_writer, PROFILE_CSV_HEADER_ITEMS)

        if is_a_deep_crawl:
            self.posts_csv_file = open(
                os.path.join(self.csv_path, "posts_data.csv"), "w"
            )
            self.posts_writer = csv.writer(self.posts_csv_file)
            self.write_csv_header(self.posts_writer, POSTS_CSV_HEADER_ITEMS)

    def start_requests(self):
        self.load_web_site(INSTAGRAM_START_PAGE)
        self.log_in()
        self.search_for_username(self.username)

        yield self.parse_profile()
        self.profile_csv_file.close()

        if self.is_a_deep_crawl:
            urls_of_posts_to_crawl = self.urls_of_posts_to_crawl()

            for url_of_post in urls_of_posts_to_crawl:
                yield self.parse_post(url_of_post)
            self.posts_csv_file.close()

        sleep(next(CRAWL_FINISHED_SLEEP))
        self.driver.close()

    def parse_profile(self):
        item_loader = ItemLoader(item=ProfileDataItem())
        selector = Selector(text=self.driver.page_source)

        try:
            name_of_profile = self.username
            number_of_posts = self.number_of_posts(selector)
            followers = self.followers(selector)
            following = self.following(selector)
            description_of_profile = self.description_of_profile(selector)
            hashtags_of_description = self.hashtags_of_description(selector)
            other_tags_of_description = self.other_tags_of_description(selector)
            lifestyle_stories = self.lifestyle_stories(selector)
            if self.is_a_deep_crawl:
                following_names = self.following_names(following)
        except IndexError:
            pass

        self.load_profile_items(
            item_loader,
            name_of_profile,
            number_of_posts,
            followers,
            following,
            description_of_profile,
            hashtags_of_description,
            other_tags_of_description,
            lifestyle_stories,
            following_names,
        )

        self.write_csv_profile_item(item_loader)

    def parse_post(self, url_of_post):
        self.load_web_site(url_of_post)
        # TODO Ponder: Is the item loader even worth it? i mean maybe for pipelines but...
        item_loader = ItemLoader(item=PostDataItem())
        selector = Selector(text=self.driver.page_source)

        try:
            id_of_post = self.id_of_post(url_of_post)
            likes_of_post = self.likes_of_post(selector)
            hashtags_of_post = self.hashtags_of_post()
            description_of_post = self.description_of_post(selector)
            post_was_liked_by = self.post_was_liked_by(likes_of_post)
            date_of_post = self.date_of_post(selector)
        except IndexError:
            post_was_liked_by = None

        self.load_post_items(
            item_loader,
            id_of_post,
            url_of_post,
            likes_of_post,
            hashtags_of_post,
            description_of_post,
            post_was_liked_by,
            date_of_post,
        )

        self.write_csv_post_item(item_loader)
        # TODO BUG: again, sometimes it doesn't load the whole page, as it was on post_was_liked_by
        try:
            url_of_image = self.url_of_image()
            self.download_images(id_of_post, url_of_image)
        except IndexError:
            pass

    # =========================== Log in ===========================
    def log_in(self):
        self.accept_cookies()
        self.enter_username_and_password()
        self.press_submit_button()
        self.deny_save_login_info()
        self.deny_turn_on_notifications()

    def accept_cookies(self):
        accept_all_cookies = WebDriverWait(self.driver, SECONDS_UNTIL_TIMEOUT).until(
            EC.element_to_be_clickable((By.XPATH, '//button[text()="Accept All"]'))
        )
        # TODO Ponder: Is this nice this way or just work with comments?
        #  -> actually we dont require it because methods right @Thomas?
        accept_all_cookies.click()
        sleep(next(CLICK_SLEEP))

    def enter_username_and_password(self):
        log_in_username = WebDriverWait(self.driver, SECONDS_UNTIL_TIMEOUT).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']"))
        )

        log_in_password = WebDriverWait(self.driver, SECONDS_UNTIL_TIMEOUT).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']"))
        )

        log_in_username.clear()
        log_in_password.clear()
        log_in_username.send_keys(LOG_IN_USERNAME)
        log_in_password.send_keys(LOG_IN_PASSWORD)
        sleep(next(ENTER_DATA_SLEEP))

    def press_submit_button(self):
        WebDriverWait(self.driver, SECONDS_UNTIL_TIMEOUT).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        ).click()
        sleep(next(CLICK_SLEEP))

    def deny_save_login_info(self):
        WebDriverWait(self.driver, SECONDS_UNTIL_TIMEOUT).until(
            EC.element_to_be_clickable(
                (By.XPATH, '//button[contains(text(), "Not Now")]')
            )
        ).click()
        sleep(next(CLICK_SLEEP))

    def deny_turn_on_notifications(self):
        WebDriverWait(self.driver, SECONDS_UNTIL_TIMEOUT).until(
            EC.element_to_be_clickable(
                (By.XPATH, '//button[contains(text(), "Not Now")]')
            )
        ).click()
        sleep(next(CLICK_SLEEP))

    # =========================== Search and process to user profile ===========================
    def search_for_username(self, username):
        search_box = WebDriverWait(self.driver, SECONDS_UNTIL_TIMEOUT).until(
            EC.element_to_be_clickable((By.XPATH, XPATH_TO_SEARCH_FOR_USERNAME_BOX))
        )
        sleep(next(CLICK_SLEEP))
        self.enter_username_in_search_box(search_box, username)
        self.process_to_profile(search_box)

    def enter_username_in_search_box(self, search_box, username):
        search_box.clear()
        search_box.send_keys(username)
        sleep(next(ENTER_DATA_SLEEP))

    def process_to_profile(self, search_box):
        search_box.send_keys(Keys.ENTER)
        search_box.send_keys(Keys.ENTER)
        sleep(next(WAIT_FOR_RESPONSE_SLEEP))

    # =========================== Crawl for profile data ===========================
    def number_of_posts(self, selector):
        return selector.xpath(XPATH_TO_PROFILE_NUMBER_OF_POSTS).extract()[0]

    def followers(self, selector):
        return selector.xpath(XPATH_TO_PROFILE_FOLLOWERS).extract()[1]

    def following(self, selector):
        return selector.xpath(XPATH_TO_PROFILE_FOLLOWING).extract()[2]

    def description_of_profile(self, selector):
        return selector.xpath(XPATH_TO_PROFILE_DESCRIPTION).extract()

    def hashtags_of_description(self, selector):
        other_tags = selector.xpath(XPATH_TO_PROFILE_HASHTAGS).extract()
        hashtags = [tag for tag in other_tags if "#" in tag]
        return hashtags

    def other_tags_of_description(self, selector):
        other_tags = selector.xpath(XPATH_TO_PROFILE_OTHER_TAGS).extract()
        other_tags = [tag for tag in other_tags if "#" not in tag]
        return other_tags

    def lifestyle_stories(self, selector):
        return selector.xpath(XPATH_TO_PROFILE_LIFESTYLE_STORIES).extract()

    def following_names(self, following):  # TODO Refactor, pretty close to post_was_liked_by
        # TODO Ask: if we would extract the method there would be many attributes, what is the pythonic way?
        following_box = self.driver.find_elements_by_xpath(XPATH_TO_POST_FOLLOWING_BOX)
        following_names = set()
        last_element_inside_popup = None
        penultimate_element_inside_popup = None
        counter = 0  # TODO delete

        following_box[2].click()
        sleep(next(WAIT_FOR_RESPONSE_SLEEP))
        while int(following) > len(following_names):
            selector = Selector(text=self.driver.page_source)
            current_users = selector.xpath(
                XPATH_TO_POST_USERS_WHO_ARE_FOLLOWED
            ).extract()
            for user in current_users:
                following_names.add(user)

            current_element_inside_popup = self.element_inside_following_popup()
            self.scroll_down_popup(current_element_inside_popup)
            if (
                    current_element_inside_popup == last_element_inside_popup
                    or current_element_inside_popup == penultimate_element_inside_popup
            ):
                break
                # TODO Ask: its so ugly but it always jumped between the last and the last last, any idea why?
            penultimate_element_inside_popup = last_element_inside_popup
            last_element_inside_popup = current_element_inside_popup
            counter += 1  # TODO delete

        self.driver.find_elements_by_xpath('//*[@class="QBdPU "]')[1].click()
        return following_names

    # =========================== Fetch URLs ===========================
    def urls_of_posts_to_crawl(self) -> set:
        cleaned_urls_of_posts = set()

        while True:
            self.scroll_down()
            page_height = self.driver.execute_script(PAGE_HEIGHT_SCRIPT)
            total_scrolled_height = self.driver.execute_script(
                TOTAL_SCROLLED_HEIGHT_SCRIPT
            )

            for cleaned_url in self.cleaned_urls_of_posts():
                cleaned_urls_of_posts.add(cleaned_url)
            if page_height - 1 <= total_scrolled_height:
                break

        return cleaned_urls_of_posts

    # =========================== Scrolling ===========================
    # TODO Implement: make it dynamically, eg 2/3 times down for 40-60, 1 time up all random -> AND go to the end of site
    # TODO Ponder: is this even neccessary? Are we even requesting new data? Aka does it even know the difference if we scroll up/down?
    def scroll_down(self):
        # for _ in range (10):
        #     if next(SCROLL_UPWARDS):
        #         self.driver.execute_script(f"window.scrollBy(0, {-next(SCROLL_LENGTH_ON_WEBSITE)});")
        #     else:
        #         self.driver.execute_script(f"window.scrollBy(0, {next(SCROLL_LENGTH_ON_WEBSITE)});")
        self.driver.execute_script(
            f"window.scrollBy(0, {next(SCROLL_LENGTH_ON_WEBSITE)});"
        )
        sleep(next(ENTER_DATA_SLEEP))

    def scroll_down_popup(self, element_inside_popup):
        element_inside_popup.send_keys(Keys.DOWN * next(SCROLL_LENGTH_INSIDE_POPUP))
        sleep(next(CLICK_SLEEP))

        return element_inside_popup

    def element_inside_likes_popup(self):
        elements_inside_popup = self.driver.find_elements_by_xpath(
            XPATH_TO_POST_ELEMENT_INSIDE_LIKES_POPUP
        )
        element_inside_popup = elements_inside_popup[-1:][
            0
        ]  # TODO BUG: sometimes the "likes" field doesn't get loaded
        return element_inside_popup

    def element_inside_following_popup(self):  # TODO Refactor, pretty close to element_inside_likes_popup
        elements_inside_popup = self.driver.find_elements_by_xpath(
            XPATH_TO_POST_ELEMENT_INSIDE_FOLLOWING_POPUP
        )
        element_inside_popup = elements_inside_popup[-1:][
            0
        ]  # TODO BUG: sometimes the "following" field doesn't get loaded
        return element_inside_popup

    # =========================== Fetch posts ===========================
    # TODO Ask: Thomas is this worth/nice for readability? with -> list
    def cleaned_urls_of_posts(
        self,
    ) -> list:
        urls_of_posts = self.urls_of_posts()
        cleaned_image_urls = [
            cleaned_url
            for cleaned_url in urls_of_posts
            if "/p/" in cleaned_url  # "/p/" indicates that it is a post href
        ]
        return cleaned_image_urls

    def urls_of_posts(self) -> list:
        # images = self.driver.find_elements_by_tag_name("img")  # TODO Refactor: Look this up in docu.
        urls_of_posts = self.driver.find_elements_by_xpath("//a")
        urls_of_posts = [
            url_of_post.get_attribute("href") for url_of_post in urls_of_posts
        ]

        return urls_of_posts

    # =========================== Crawl for posts data ===========================
    def id_of_post(self, url_of_post):
        return url_of_post.split("/p/")[1].split("/")[0]

    def likes_of_post(self, selector):
        return selector.xpath(XPATH_TO_POST_LIKES).extract_first()

    def hashtags_of_post(self):
        hashtags = self.driver.find_elements_by_xpath(XPATH_TO_POST_HASHTAGS)
        hashtags = [hashtag.get_attribute("innerHTML") for hashtag in hashtags]
        return hashtags

    def description_of_post(self, selector):
        return selector.xpath(XPATH_TO_POST_DESCRIPTION).extract()

    def post_was_liked_by(self, likes_of_post):
        likes_box = self.driver.find_elements_by_xpath(XPATH_TO_POST_LIKES_BOX)
        post_was_liked_by = set()
        last_element_inside_popup = None
        penultimate_element_inside_popup = None

        if len(likes_box) > 0:
            likes_box[0].click()
            sleep(next(WAIT_FOR_RESPONSE_SLEEP))
            while int(likes_of_post) > len(post_was_liked_by):
                selector = Selector(text=self.driver.page_source)
                current_users = selector.xpath(
                    XPATH_TO_POST_USERS_WHO_LIKED_IT
                ).extract()
                # [people_liked_post.add(user) for user in temp_users] # TODO Ask: why this doesn't work?
                for user in current_users:
                    post_was_liked_by.add(user)

                # TODO Ask: better solution @Thomas?
                current_element_inside_popup = self.element_inside_likes_popup()
                self.scroll_down_popup(current_element_inside_popup)
                if (
                    current_element_inside_popup == last_element_inside_popup
                    or current_element_inside_popup == penultimate_element_inside_popup
                ):
                    break
                # TODO Ask: its so ugly but it always jumped between the last and the last last, any idea why?
                penultimate_element_inside_popup = last_element_inside_popup
                last_element_inside_popup = current_element_inside_popup

        return post_was_liked_by

    def date_of_post(self, selector):
        return selector.xpath(XPATH_TO_POST_DATE).extract_first()

    def url_of_image(self):
        return self.driver.find_elements_by_tag_name("img")[1].get_attribute("src")

        # =========================== Handle CSV and images ===========================

    def write_csv_header(self, writer, header_items):
        writer.writerow(header_items)

    def write_csv_profile_item(self, item_loader):
        self.profile_writer.writerow(
            [
                " ".join(item_loader.get_collected_values(NAME_OF_PROFILE)),
                " ".join(item_loader.get_collected_values(NUMBER_OF_POSTS)),
                " ".join(item_loader.get_collected_values(FOLLOWERS)),
                " ".join(item_loader.get_collected_values(FOLLOWING)),
                " ".join(item_loader.get_collected_values(DESCRIPTION_OF_PROFILE)),
                " ".join(item_loader.get_collected_values(HASHTAGS_OF_DESCRIPTION)),
                " ".join(item_loader.get_collected_values(OTHER_TAGS_OF_DESCRIPTION)),
                " ".join(item_loader.get_collected_values(LIFESTYLE_STORIES)),
                " ".join(item_loader.get_collected_values(FOLLOWING_NAMES)),
            ]
        )
        self.profile_csv_file.flush()

    def write_csv_post_item(self, item_loader):
        # TODO Ask: Is there a better way for the next 2 lines?
        item_loader_likes_of_post = item_loader.get_collected_values(LIKES_OF_POST)
        item_loader_post_was_liked_by = item_loader.get_collected_values(
            POST_WAS_LIKED_BY
        )
        self.posts_writer.writerow(
            [
                " ".join(item_loader.get_collected_values(ID_OF_POST)),
                " ".join(item_loader.get_collected_values(URL_OF_POST)),
                " ".join(item_loader_likes_of_post)
                if len(item_loader_likes_of_post) > 0
                else None,
                " ".join(item_loader.get_collected_values(HASHTAGS_OF_POST)),
                " ".join(item_loader.get_collected_values(DESCRIPTION_OF_POST)),
                " ".join(item_loader_post_was_liked_by)
                if len(item_loader_likes_of_post) > 0
                else None,
                " ".join(item_loader.get_collected_values(DATE_OF_POST)),
            ]
        )
        self.posts_csv_file.flush()  # TODO maybe delete if we dont need to safe during runtime

    def download_images(self, id_of_post, url_of_image):
        save_to_location = os.path.join(self.image_path, id_of_post + ".jpg")
        wget.download(url_of_image, save_to_location)

    # =========================== Utility ===========================
    def start_webdriver(self, working_directory):
        webdriver_path = os.path.join(
            working_directory, os.pardir, os.pardir, "chromedriver"
        )
        self.driver = webdriver.Chrome(webdriver_path)

    def load_web_site(self, url):
        self.driver.get(url)
        sleep(next(WAIT_FOR_RESPONSE_SLEEP))

    def load_post_items(
        self,
        item_loader,
        id_of_post,
        url_of_post,
        likes_of_post,
        hashtags_of_post,
        description_of_post,
        post_was_liked_by,
        date_of_post,
    ):
        # TODO Refactor: maybe a function or something? eg string + data in a dict then iteratre over it?
        # TODO Ask: Thomas best solution?
        item_loader.add_value(ID_OF_POST, id_of_post)
        item_loader.add_value(URL_OF_POST, url_of_post)
        item_loader.add_value(LIKES_OF_POST, likes_of_post)
        item_loader.add_value(HASHTAGS_OF_POST, hashtags_of_post)
        item_loader.add_value(DESCRIPTION_OF_POST, description_of_post)
        item_loader.add_value(POST_WAS_LIKED_BY, post_was_liked_by)
        item_loader.add_value(DATE_OF_POST, date_of_post)

        item_loader.load_item()

    # TODO Ask: is there a better way? because the code is pretty close
    def load_profile_items(
        self,
        item_loader,
        name_of_profile,
        number_of_posts,
        followers,
        following,
        description_of_profile,
        hashtags_of_description,
        other_tags_of_description,
        lifestyle_stories,
            following_names,
    ):
        item_loader.add_value(NAME_OF_PROFILE, name_of_profile)
        item_loader.add_value(NUMBER_OF_POSTS, number_of_posts)
        item_loader.add_value(FOLLOWERS, followers)
        item_loader.add_value(FOLLOWING, following)
        item_loader.add_value(DESCRIPTION_OF_PROFILE, description_of_profile)
        item_loader.add_value(HASHTAGS_OF_DESCRIPTION, hashtags_of_description)
        item_loader.add_value(OTHER_TAGS_OF_DESCRIPTION, other_tags_of_description)
        item_loader.add_value(LIFESTYLE_STORIES, lifestyle_stories)
        item_loader.add_value(FOLLOWING_NAMES, following_names)

        item_loader.load_item()

    def create_directory(self, path):
        if not os.path.exists(path):
            os.makedirs(path)
