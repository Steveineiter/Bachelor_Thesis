# Selenium imports
import csv

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from parsel import Selector


# Other imports
import os
import wget
import scrapy
from time import sleep

# my packages
from ..constants import *


class TwitterUserSpider(scrapy.Spider):
    name = "twitter_user_spider"
    allowed_domains = ["twitter.com"]
    start_urls = ["https://twitter.com/Lipton"]

    def __init__(self):
        self.working_directory = os.getcwd()
        webdriver_path = os.path.join(self.working_directory, os.pardir, "chromedriver")
        self.driver = webdriver.Chrome(webdriver_path)

    def start_requests(self):
        self.driver.get(TWITTER_START_PAGE)

        # Logging in
        # login_xpath = '//*[@class="css-4rbku5 css-18t94o4 css-1dbjc4n r-1m3jxhj r-42olwf r-sdzlij r-1phboty r-rs99b7 r-1loqt21 r-1mnahxq r-19yznuf r-64el8z r-1ny4l3l r-1dye5f7 r-o7ynqc r-6416eg r-lrvibr"]'
        # WebDriverWait(self.driver, 20).until(
        #     EC.element_to_be_clickable((By.XPATH, login_xpath))
        # ).click()

        username_field = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "input[name='session[username_or_email]']")
            )
        )
        password_field = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "input[name='session[password]']")
            )
        )
        username_field.clear()
        password_field.clear()

        username_field.send_keys("s.schoerkmeier@gmx.at")
        password_field.send_keys("!23Juli1996!")
        sleep(0.5)

        login_field_xpath = '//*[@class="css-18t94o4 css-1dbjc4n r-42olwf r-sdzlij r-1phboty r-rs99b7 r-1fz3rvf r-usiww2 r-19yznuf r-64el8z r-1ny4l3l r-1dye5f7 r-o7ynqc r-6416eg r-lrvibr"]'
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, login_field_xpath))
        ).click()
        sleep(next(ENTER_DATA_SLEEP))

        # Load liption twitter page
        self.driver.get(TWITTER_LIPTON_PAGE)
        sleep(next(WAIT_FOR_RESPONSE_SLEEP))

        # Load followers page
        followers_xpath = '//*[@class="css-4rbku5 css-18t94o4 css-901oao r-18jsvk2 r-1loqt21 r-1qd0xha r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-qvutc0"]'
        self.driver.find_elements_by_xpath(followers_xpath)[1].click()
        sleep(2)

        urls_of_users_following = self.urls_of_users_following()

        self.safe_in_csv(urls_of_users_following)

        self.driver.close()

    def safe_in_csv(self, urls_of_users_following):
        with open(
            "/home/stefan/Knowledge/Bachelor-thesis/twitter_scraper/twitter_scraper/items/twitter_usernames_and_urls.csv", "w", newline=""
        ) as hashtags_likes_correlation_csv_file:
            fieldnames = ["username", "url"]
            dict_writer = csv.DictWriter(
                hashtags_likes_correlation_csv_file, fieldnames=fieldnames
            )

            dict_writer.writeheader()
            for url in urls_of_users_following:
                username = url.split("https://twitter.com/")[1]
                dict_writer.writerow(
                    {
                        "username": username,
                        "url": url,
                    }
                )

    # ========================== Utility ===========================
    def urls_of_users_following(self) -> set:
        urls_of_users = set()
        is_post_limit_reached = False

        while True:
            self.scroll_down()
            page_height = self.driver.execute_script(PAGE_HEIGHT_SCRIPT)
            total_scrolled_height = self.driver.execute_script(
                TOTAL_SCROLLED_HEIGHT_SCRIPT
            )

            for user_url in self._urls_of_users():
                urls_of_users.add(user_url)
                if len(urls_of_users) >= MAXIMAL_FOLLOWERS:
                    is_post_limit_reached = True
                    break
            if page_height - 1 <= total_scrolled_height or is_post_limit_reached:
                break

        return urls_of_users

    def _urls_of_users(self) -> list:
        urls_of_users = self.driver.find_elements_by_xpath(
            '//*[@class="css-1dbjc4n r-1wbh5a2 r-dnmrzs"]/a'
        )
        urls_of_users = [
            url_of_post.get_attribute("href") for url_of_post in urls_of_users
        ]
        return urls_of_users  # To remove duplicates.

    def scroll_down(self):
        self.driver.execute_script(
            f"window.scrollBy(0, {next(SCROLL_LENGTH_ON_WEBSITE)});"
        )
        sleep(next(ENTER_DATA_SLEEP))
