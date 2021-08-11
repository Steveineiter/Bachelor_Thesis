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
from scrapy.http import Request
from scrapy.loader import ItemLoader
from instagram_scraper.items import InstagramScraperMarryItem


from time import sleep
from instagram_scraper.constants import *


class InstagramMarrySpider(Spider):
    name = "marry_crawler"
    allowed_domains = ["instagram.com"]
    start_urls = ["http://instagram.com/"]

    def start_requests(self):
        self.driver = webdriver.Chrome(
            "/home/stefan/Knowledge/Bachelor-thesis/chromedriver"
        )
        self.driver.get("https://www.instagram.com/")

        self.log_in()
        self.search_for_username(MARRYICETEA_INSTAGRAM_USERNAME)
        self.scroll_down()
        cleaned_urls_of_posts = self.cleaned_urls_of_posts()
        for url_of_post in cleaned_urls_of_posts:
            yield self.parse_post(url_of_post)

# TODO HIER WEITER STEFI !!!!
    def parse_post(self, url_of_post):
        self.driver.get(url_of_post)
        sleep(next(WAIT_FOR_RESPONSE_SLEEP))
        selector = Selector(text=self.driver.page_source)
        item_loader = ItemLoader(item=InstagramScraperMarryItem())

        post_id = url_of_post.split("/p/")[1].split("/")[0]

        item_loader.add_value("post_id", post_id)
        item_loader.add_value("url_of_post", url_of_post)

        item_loader.load_item()

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
        accept_all_cookies.click()
        sleep(next(CLICK_SLEEP))
        # TODO Ponder: Is this nice this way or just work with comments?
        #  -> actually we dont require it because methods right @Thomas?

    def enter_username_and_password(self):
        username = WebDriverWait(self.driver, SECONDS_UNTIL_TIMEOUT).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']"))
        )

        password = WebDriverWait(self.driver, SECONDS_UNTIL_TIMEOUT).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']"))
        )

        username.clear()
        password.clear()
        username.send_keys("stefandovakin")
        password.send_keys("dragonborn123")
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

    # =========================== Search ===========================
    def search_for_username(self, username):
        search_box = WebDriverWait(self.driver, SECONDS_UNTIL_TIMEOUT).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Search']"))
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

    # =========================== Dynamic Scrolling ===========================
    # TODO Implement: make it dynamically, eg 2/3 times down for 40-60, 1 time up all random
    def scroll_down(self):
        self.driver.execute_script("window.scrollTo(0, 4000);")
        sleep(next(ENTER_DATA_SLEEP))

    # =========================== Fetch posts ===========================
    def cleaned_urls_of_posts(self) -> list: # TODO Ask: Thomas is this worth/nice for readability?
        urls_of_posts = self.urls_of_posts()
        cleaned_image_urls = [
            cleaned_url for cleaned_url in urls_of_posts if "/p/" in cleaned_url
        ]

        return cleaned_image_urls

    def urls_of_posts(self) -> list:
        # images = self.driver.find_elements_by_tag_name("img")  # TODO Refactor: Look this up in docu.
        urls_of_posts = self.driver.find_elements_by_xpath("//a")
        urls_of_posts = [url_of_post.get_attribute("href") for url_of_post in urls_of_posts]

        return urls_of_posts
