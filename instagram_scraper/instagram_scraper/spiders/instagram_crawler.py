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

from instagram_scraper.csv_handler import CSVHandler
from instagram_scraper.items import PostDataItem, ProfileDataItem


from time import sleep
from instagram_scraper.constants import *

from instagram_scraper.file_manager import FileManager


# TODO Ask: better one big file with many arguments, or 2 files with lots of duplicated code?
# TODO Ponder: do we really need those time outs by accept fields etc.? actually they are annoying.
class InstagramSpider(Spider):
    name = "instagram_crawler"
    allowed_domains = ["instagram.com"]
    start_urls = ["http://instagram.com/"]

    def __init__(
        self,
        username=MARRYICETEA_INSTAGRAM_USERNAME,
        is_a_company="True",
        is_a_deep_crawl="True",
        **kwargs,
    ):
        self.username = username
        self.is_a_company = is_a_company
        self.is_a_deep_crawl = is_a_deep_crawl
        self.already_crawled_urls = set()
        self.profile_item_loader = ItemLoader(item=ProfileDataItem())
        self.post_items_loader = ItemLoader(item=PostDataItem())
        self.csv_handler = CSVHandler()

        # TODO Ask: How to pass bool arguments in bash? Eg false?
        self.is_a_company = self.input_to_bool(self.is_a_company)
        self.is_a_deep_crawl = self.input_to_bool(self.is_a_deep_crawl)

        super().__init__(**kwargs)
        self.file_manager = FileManager(self.is_a_company, username)

        working_directory = os.getcwd()
        webdriver_path = os.path.join(
            working_directory, os.pardir, os.pardir, "chromedriver"
        )

        self.driver = webdriver.Chrome(webdriver_path)

        if is_a_deep_crawl:
            self.already_crawled_urls = self.file_manager.already_crawled_urls()

    def start_requests(self):
        self.load_web_site(INSTAGRAM_START_PAGE)
        self.log_in()
        self.search_for_username(self.username)

        if not self.file_manager.has_profile_data() or self.is_a_company:
            yield self.parse_profile()

        if self.is_a_deep_crawl:
            urls_of_posts_to_crawl = (
                self.urls_of_posts_to_crawl() - self.already_crawled_urls
            )

            for url_of_post in urls_of_posts_to_crawl:
                yield self.parse_post(url_of_post)

        self.file_manager.save_crawled_data(
            self.profile_item_loader, self.post_items_loader
        )
        self.driver.close()
        sleep(next(CRAWL_FINISHED_SLEEP))

    def parse_profile(self):
        # item_loader = ItemLoader(item=ProfileDataItem())
        selector = Selector(text=self.driver.page_source)

        try:
            profile_item = {
                NAME_OF_PROFILE: self.username,
                NUMBER_OF_POSTS: self.number_of_posts(selector),
                FOLLOWERS: self.followers(selector),
                FOLLOWING: self.following(selector),
                DESCRIPTION_OF_PROFILE: self.description_of_profile(selector),
                HASHTAGS_OF_DESCRIPTION: self.hashtags_of_description(selector),
                OTHER_TAGS_OF_DESCRIPTION: self.other_tags_of_description(selector),
                LIFESTYLE_STORIES: self.lifestyle_stories(selector),
                IS_PRIVATE: "True" if self.is_private(selector) else None,
            }
            profile_item[FOLLOWING_NAMES] = (
                self.following_names(profile_item[FOLLOWING])
                if self.is_a_deep_crawl and not profile_item[IS_PRIVATE]
                else None
            )
            # TODO Implement this after Refactor because it should be the same as following_names
            profile_item[FOLLOWERS_NAMES] = (
                self.followers_name(profile_item[FOLLOWERS])
                if self.is_a_deep_crawl and self.is_a_company
                else None
            )

            self.load_item_from_dictionary(self.profile_item_loader, profile_item)
        except IndexError:
            pass

    def parse_post(self, url_of_post):
        self.load_web_site(url_of_post)
        selector = Selector(text=self.driver.page_source)

        try:
            post_items = {
                ID_OF_POST: self.id_of_post(url_of_post),
                URL_OF_POST: url_of_post,
                LIKES_OF_POST: self.likes_of_post(selector),
                HASHTAGS_OF_POST: self.hashtags_of_post(),
                DESCRIPTION_OF_POST: self.description_of_post(selector),
                DATE_OF_POST: self.date_of_post(selector),
            }
            post_items[POST_WAS_LIKED_BY] = (
                self.post_was_liked_by(post_items[LIKES_OF_POST])
                if self.is_a_company
                else None
            )

            self.load_item_from_dictionary(self.post_items_loader, post_items)
        except IndexError:
            pass

    # =========================== Log in ===========================
    def log_in(self):
        self.accept_cookies()
        self.enter_username_and_password()
        self.press_submit_button()
        try:
            self.deny_save_login_info()
            self.deny_turn_on_notifications()
        except EC.WebDriverException:
            pass

    def accept_cookies(self):
        try:
            accept_all_cookies = WebDriverWait(
                self.driver, SECONDS_UNTIL_TIMEOUT
            ).until(
                EC.element_to_be_clickable((By.XPATH, '//button[text()="Accept All"]'))
            )
            # TODO Ponder: Is this nice this way or just work with comments?
            #  -> actually we dont require it because methods right @Thomas?
            accept_all_cookies.click()
        except EC.WebDriverException:
            pass
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

    def is_private(self, selector):
        is_private_field_set = selector.xpath(XPATH_TO_PROFILE_IS_PRIVATE).extract()
        if is_private_field_set:
            return True
        else:
            return False

    def following_names(
        self, following
    ):  # TODO Refactor, pretty close to post_was_liked_by
        # TODO sometimes it doesnt get loaded, we need more sleep?
        # TODO Ask: if we would extract the method there would be many attributes, what is the pythonic way?
        following_box = self.driver.find_elements_by_xpath(XPATH_TO_POST_FOLLOWING_BOX)
        following_names = set()
        last_element_inside_popup = None
        penultimate_element_inside_popup = None

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
            sleep(next(CLICK_SLEEP))

        self.driver.find_elements_by_xpath(XPATH_TO_PROFILE_FOLLOWING_EXIT_BUTTON)[
            1
        ].click()
        return following_names

    def followers_name(self, followers):
        return "Foo"

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
                if (
                    not self.is_a_company
                    and len(cleaned_urls_of_posts) >= MAXIMAL_POSTS_OF_CONSUMERS  # TODO REFACTOR
                ):
                    break
            if page_height - 1 <= total_scrolled_height or (
                not self.is_a_company
                and len(cleaned_urls_of_posts) >= MAXIMAL_POSTS_OF_CONSUMERS
            ):
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

    def element_inside_following_popup(
        self,
    ):  # TODO Refactor, pretty close to element_inside_likes_popup
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

    # =========================== Utility ===========================
    @staticmethod
    def input_to_bool(user_input: str):
        user_input_in_uppercase = user_input.upper()
        if (
            user_input_in_uppercase == "FALSE"
            or user_input_in_uppercase == "F"
            or user_input_in_uppercase == "0"
        ):
            return False
        return True

    def start_webdriver(self, working_directory):
        webdriver_path = os.path.join(
            working_directory, os.pardir, os.pardir, "chromedriver"
        )
        self.driver = webdriver.Chrome(webdriver_path)

    def load_web_site(self, url):
        self.driver.get(url)
        sleep(next(WAIT_FOR_RESPONSE_SLEEP))

    @staticmethod
    def load_item_from_dictionary(item_loader: ItemLoader, dictionary: dict):
        for key, value in dictionary.items():
            item_loader.add_value(key, value)
        item_loader.load_item()

    def create_directory(self, path):
        if not os.path.exists(path):
            os.makedirs(path)
