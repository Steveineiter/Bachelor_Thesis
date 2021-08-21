# Project classes
from instagram_scraper.csv_handler import CSVHandler
from instagram_scraper.items import PostDataItem, ProfileDataItem
from instagram_scraper.constants import *
from instagram_scraper.file_manager import FileManager

# Selenium imports
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

# Other imports
import os
from abc import ABC
from time import sleep
from scrapy import Spider
from parsel import Selector
from scrapy.loader import ItemLoader


class InstagramSpider(Spider, ABC):
    name = "instagram_crawler"
    allowed_domains = ["instagram.com"]
    start_urls = ["https://instagram.com/"]

    def __init__(
        self,
        username=MARRYICETEA_INSTAGRAM_USERNAME,
        is_a_company="True",
        is_a_deep_crawl="True",
        user_count_to_load_from_csv=0,
        path_to_users_to_crawl_csv=None,
        is_raspberry_pi=False,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.usernames = [username]
        self.is_a_company = self.input_to_bool(is_a_company)
        self.is_a_deep_crawl = self.input_to_bool(is_a_deep_crawl)
        self.user_count_to_load_from_csv = int(user_count_to_load_from_csv)
        self.already_crawled_urls = set()
        self.csv_handler = CSVHandler()
        self.path_to_user_to_crawl_csv = path_to_users_to_crawl_csv

        self.working_directory = os.getcwd()
        if is_raspberry_pi:
            webdriver_path = "/usr/lib/chromium-browser/chromedriver"
        else:
            webdriver_path = os.path.join(
                self.working_directory, os.pardir, "chromedriver"
            )
        self.driver = webdriver.Chrome(webdriver_path)

    def start_requests(self):
        self.load_web_site(INSTAGRAM_START_PAGE)
        self.log_in()

        if self.user_count_to_load_from_csv:
            # TODO Refactor
            path_to_users_to_crawl_csv = os.path.join(
                self.working_directory, "users_to_crawl.csv"
            )
            self.usernames = self.csv_handler.users_from_csv(
                path_to_users_to_crawl_csv, self.user_count_to_load_from_csv
            )

        for username in self.usernames:
            file_manager = FileManager(self.is_a_company, username)
            file_manager.create_directories()

            self.search_for_username(username)

            if self.is_a_company or not file_manager.has_profile_data():
                yield self.parse_profile(username, file_manager)

            if self.is_a_deep_crawl:
                already_crawled_urls = file_manager.already_crawled_urls()

                urls_of_posts_to_crawl = (
                    self.urls_of_posts_to_crawl() - already_crawled_urls
                )
                for url_of_post in urls_of_posts_to_crawl:
                    yield self.parse_post(url_of_post, file_manager)

            if self.path_to_user_to_crawl_csv:
                file_manager.delete_row_from_user_to_crawl_csv(
                    self.path_to_user_to_crawl_csv
                )
            sleep(next(CRAWL_FINISHED_SLEEP))

        self.driver.close()

    def parse_profile(self, username, file_manager):
        profile_item_loader = ItemLoader(item=ProfileDataItem())
        selector = Selector(text=self.driver.page_source)

        try:
            profile_item = {
                NAME_OF_PROFILE: username,
                NUMBER_OF_POSTS: self.number_of_posts(selector),
                FOLLOWERS: self.followers(selector),
                FOLLOWING: self.following(selector),
                DESCRIPTION_OF_PROFILE: self.description_of_profile(selector),
                HASHTAGS_OF_DESCRIPTION: self.hashtags_of_description(selector),
                OTHER_TAGS_OF_DESCRIPTION: self.other_tags_of_description(selector),
                LIFESTYLE_STORIES: self.lifestyle_stories(selector),
                IS_PRIVATE: "True" if self.is_private(selector) else None,
            }
            sleep(next(WAIT_FOR_RESPONSE_SLEEP))
            # TODO ponder make it with flag? for POC we don't need them at users.
            profile_item[FOLLOWING_NAMES] = (
                # self.following_names(profile_item[FOLLOWING])
                # if self.is_a_deep_crawl and not profile_item[IS_PRIVATE]
                # else None
                None
            )
            sleep(next(WAIT_FOR_RESPONSE_SLEEP))
            profile_item[FOLLOWERS_NAMES] = (
                # self.followers_name(profile_item[FOLLOWERS])
                # if self.is_a_deep_crawl and self.is_a_company
                # else None
                None
            )

            self.load_item_from_dictionary(profile_item_loader, profile_item)
            file_manager.safe_profile_data(profile_item_loader)

        except IndexError:
            pass

    def parse_post(self, url_of_post, file_manager):
        self.load_web_site(url_of_post)
        sleep(next(WAIT_FOR_RESPONSE_SLEEP))
        selector = Selector(text=self.driver.page_source)
        post_items_loader = ItemLoader(item=PostDataItem())

        try:
            post_items = {
                ID_OF_POST: self.id_of_post(url_of_post),
                URL_OF_POST: url_of_post,
                LIKES_OF_POST: self.likes_of_post(selector),
                HASHTAGS_OF_POST: self.hashtags_of_post(),
                DESCRIPTION_OF_POST: self.description_of_post(selector),
                DATE_OF_POST: self.date_of_post(selector),
            }
            sleep(next(WAIT_FOR_RESPONSE_SLEEP))
            post_items[POST_WAS_LIKED_BY] = (
                self.post_was_liked_by(post_items[LIKES_OF_POST])
                if self.is_a_company
                else None
            )
            sleep(next(WAIT_FOR_RESPONSE_SLEEP))

            self.load_item_from_dictionary(post_items_loader, post_items)
            file_manager.safe_post_data(post_items_loader)
            file_manager.safe_image(post_items_loader)
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
        except expected_conditions.WebDriverException:
            pass

    def accept_cookies(self):
        try:
            WebDriverWait(self.driver, SECONDS_UNTIL_TIMEOUT).until(
                expected_conditions.element_to_be_clickable(
                    (By.XPATH, '//button[text()="Accept All"]')
                )
            ).click()
        except expected_conditions.WebDriverException:
            pass
        sleep(next(CLICK_SLEEP))

    def enter_username_and_password(self):
        log_in_username = WebDriverWait(self.driver, SECONDS_UNTIL_TIMEOUT).until(
            expected_conditions.element_to_be_clickable(
                (By.CSS_SELECTOR, "input[name='username']")
            )
        )

        log_in_password = WebDriverWait(self.driver, SECONDS_UNTIL_TIMEOUT).until(
            expected_conditions.element_to_be_clickable(
                (By.CSS_SELECTOR, "input[name='password']")
            )
        )

        log_in_username.clear()
        log_in_password.clear()
        log_in_username.send_keys(LOG_IN_USERNAME)
        log_in_password.send_keys(LOG_IN_PASSWORD)
        sleep(next(ENTER_DATA_SLEEP))

    def press_submit_button(self):
        WebDriverWait(self.driver, SECONDS_UNTIL_TIMEOUT).until(
            expected_conditions.element_to_be_clickable(
                (By.CSS_SELECTOR, "button[type='submit']")
            )
        ).click()
        sleep(next(CLICK_SLEEP))

    def deny_save_login_info(self):
        WebDriverWait(self.driver, SECONDS_UNTIL_TIMEOUT).until(
            expected_conditions.element_to_be_clickable(
                (By.XPATH, '//button[contains(text(), "Not Now")]')
            )
        ).click()
        sleep(next(CLICK_SLEEP))

    def deny_turn_on_notifications(self):
        WebDriverWait(self.driver, SECONDS_UNTIL_TIMEOUT).until(
            expected_conditions.element_to_be_clickable(
                (By.XPATH, '//button[contains(text(), "Not Now")]')
            )
        ).click()
        sleep(next(CLICK_SLEEP))

    # =========================== Search and process to user profile ===========================
    def search_for_username(self, username):
        search_box = WebDriverWait(self.driver, SECONDS_UNTIL_TIMEOUT).until(
            expected_conditions.element_to_be_clickable(
                (By.XPATH, XPATH_TO_SEARCH_FOR_USERNAME_BOX)
            )
        )
        sleep(next(CLICK_SLEEP))
        self.enter_username_in_search_box(search_box, username)
        self.process_to_profile(search_box)

    @staticmethod
    def enter_username_in_search_box(search_box, username):
        search_box.clear()
        search_box.send_keys(username)
        sleep(next(ENTER_DATA_SLEEP))

    @staticmethod
    def process_to_profile(search_box):
        search_box.send_keys(Keys.ENTER)
        search_box.send_keys(Keys.ENTER)
        sleep(next(WAIT_FOR_RESPONSE_SLEEP))

    # =========================== Crawl for profile data ===========================
    @staticmethod
    def number_of_posts(selector):
        return selector.xpath(XPATH_TO_PROFILE_NUMBER_OF_POSTS).extract()[0]

    @staticmethod
    def followers(selector):
        return selector.xpath(XPATH_TO_PROFILE_FOLLOWERS).extract()[1]

    @staticmethod
    def following(selector):
        return selector.xpath(XPATH_TO_PROFILE_FOLLOWING).extract()[2]

    @staticmethod
    def description_of_profile(selector):
        return selector.xpath(XPATH_TO_PROFILE_DESCRIPTION).extract()

    @staticmethod
    def hashtags_of_description(selector):
        other_tags = selector.xpath(XPATH_TO_PROFILE_HASHTAGS).extract()
        hashtags = [tag for tag in other_tags if "#" in tag]
        return hashtags

    @staticmethod
    def other_tags_of_description(selector):
        other_tags = selector.xpath(XPATH_TO_PROFILE_OTHER_TAGS).extract()
        other_tags = [tag for tag in other_tags if "#" not in tag]
        return other_tags

    @staticmethod
    def lifestyle_stories(selector):
        return selector.xpath(XPATH_TO_PROFILE_LIFESTYLE_STORIES).extract()

    @staticmethod
    def is_private(selector):
        is_private_field_set = selector.xpath(XPATH_TO_PROFILE_IS_PRIVATE).extract()
        if is_private_field_set:
            return True
        else:
            return False

    def following_names(self, following):
        following_names = self.user_names_from_pop_up(
            XPATH_TO_POST_FOLLOWING_BOX,
            XPATH_TO_POST_USERS_WHO_WE_FOLLOW,
            POSITION_OF_FOLLOWING_BOX,
            int(following),
            XPATH_TO_POST_ELEMENT_INSIDE_FOLLOWING_POPUP,
        )
        self.driver.find_elements_by_xpath(XPATH_TO_PROFILE_POPUP_EXIT_BUTTON)[
            1
        ].click()

        return following_names

    def followers_name(self, followers):
        followers = "".join([digit for digit in followers if digit.isdigit()])
        followers_name = self.user_names_from_pop_up(
            XPATH_TO_POST_FOLLOWERS_BOX,
            XPATH_TO_POST_USERS_WHO_FOLLOW_US,
            POSITION_OF_FOLLOWERS_BOX,
            int(followers),
            XPATH_TO_POST_ELEMENT_INSIDE_FOLLOWERS_POPUP,
        )
        self.driver.find_elements_by_xpath(XPATH_TO_PROFILE_POPUP_EXIT_BUTTON)[
            1
        ].click()

        return followers_name

    # =========================== Fetch URLs ===========================
    def urls_of_posts_to_crawl(self) -> set:
        cleaned_urls_of_posts = set()
        is_post_limit_reached = False

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
                    and len(cleaned_urls_of_posts) >= MAXIMAL_POSTS_OF_CONSUMERS
                ):
                    is_post_limit_reached = True
                    break
            if page_height - 1 <= total_scrolled_height or is_post_limit_reached:
                break

        return cleaned_urls_of_posts

    # =========================== Scrolling ===========================
    def scroll_down(self):
        self.driver.execute_script(
            f"window.scrollBy(0, {next(SCROLL_LENGTH_ON_WEBSITE)});"
        )
        sleep(next(ENTER_DATA_SLEEP))

    @staticmethod
    def scroll_down_popup(element_inside_popup):
        element_inside_popup.send_keys(Keys.DOWN * next(SCROLL_LENGTH_INSIDE_POPUP))
        sleep(next(CLICK_SLEEP))

        return element_inside_popup

    def element_inside_popup(self, xpath_to_element_inside_popup):
        # TODO BUG: sometimes the "following" field doesn't get loaded
        elements_inside_popup = self.driver.find_elements_by_xpath(
            xpath_to_element_inside_popup
        )
        element_inside_popup = elements_inside_popup[-1:][0]
        return element_inside_popup

    # =========================== Fetch posts ===========================
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
        urls_of_posts = self.driver.find_elements_by_xpath("//a")
        urls_of_posts = [
            url_of_post.get_attribute("href") for url_of_post in urls_of_posts
        ]

        return urls_of_posts

    # =========================== Crawl for posts data ===========================
    @staticmethod
    def id_of_post(url_of_post):
        return url_of_post.split("/p/")[1].split("/")[0]

    @staticmethod
    def likes_of_post(selector):
        return selector.xpath(XPATH_TO_POST_LIKES).extract_first()

    def hashtags_of_post(self):
        hashtags = self.driver.find_elements_by_xpath(XPATH_TO_POST_HASHTAGS)
        hashtags = [hashtag.get_attribute("innerHTML") for hashtag in hashtags]
        return hashtags

    @staticmethod
    def description_of_post(selector):
        return selector.xpath(XPATH_TO_POST_DESCRIPTION).extract()

    def post_was_liked_by(self, likes_of_post):
        return self.user_names_from_pop_up(
            XPATH_TO_POST_LIKES_BOX,
            XPATH_TO_POST_USERS_WHO_LIKED_IT,
            POSITION_OF_LIKES_BOX,
            int(likes_of_post),
            XPATH_TO_POST_ELEMENT_INSIDE_LIKES_POPUP,
        )

    @staticmethod
    def date_of_post(selector):
        return selector.xpath(XPATH_TO_POST_DATE).extract_first()

    def url_of_image(self):
        return self.driver.find_elements_by_tag_name("img")[1].get_attribute("src")

    # =========================== Other crawling stuff ===========================
    def user_names_from_pop_up(
        self,
        xpath_to_box,
        xpath_to_users,
        position_of_box,
        users_count,
        xpath_to_element_inside_popup,
    ):
        box_to_click = self.driver.find_elements_by_xpath(xpath_to_box)
        user_names = set()
        last_element_inside_popup = None
        penultimate_element_inside_popup = None

        if len(box_to_click) > 0:
            box_to_click[position_of_box].click()
            sleep(next(WAIT_FOR_RESPONSE_SLEEP))
            while int(users_count) > len(user_names):
                selector = Selector(text=self.driver.page_source)
                current_users = selector.xpath(xpath_to_users).extract()
                for user in current_users:
                    user_names.add(user)

                current_element_inside_popup = self.element_inside_popup(
                    xpath_to_element_inside_popup
                )
                self.scroll_down_popup(current_element_inside_popup)
                if (
                    current_element_inside_popup == last_element_inside_popup
                    or current_element_inside_popup == penultimate_element_inside_popup
                ):
                    break
                # TODO Ask: its so ugly but it always jumped between the last and the last last, any idea why?
                penultimate_element_inside_popup = last_element_inside_popup
                last_element_inside_popup = current_element_inside_popup

        return user_names

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

    def load_web_site(self, url):
        self.driver.get(url)
        sleep(next(WAIT_FOR_RESPONSE_SLEEP))

    @staticmethod
    def load_item_from_dictionary(item_loader: ItemLoader, dictionary: dict):
        for key, value in dictionary.items():
            item_loader.add_value(key, value)
        item_loader.load_item()

    @staticmethod
    def create_directory(path):
        if not os.path.exists(path):
            os.makedirs(path)
