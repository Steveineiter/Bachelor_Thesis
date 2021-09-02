# Selenium imports
import random

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


# Generators:
def random_int_generator(lower_limit, upper_limit):
    while True:
        yield random.randint(lower_limit, upper_limit)


def random_double_generator(lower_limit, upper_limit):
    while True:
        yield round(random.uniform(lower_limit, upper_limit), 2)


# ======================= Followers workbench ==============================
# Constants:
TWITTER_START_PAGE = "https://twitter.com/login"
TWITTER_LIPTON_PAGE = "https://www.twitter.com/lipton"
PAGE_HEIGHT_SCRIPT = "return document.body.scrollHeight"
TOTAL_SCROLLED_HEIGHT_SCRIPT = "return window.pageYOffset + window.innerHeight"
MAXIMAL_FOLLOWERS = 1000
SCROLL_LENGTH_ON_WEBSITE = random_int_generator(2000, 4000)
ENTER_DATA_SLEEP = random_double_generator(
    1, 3
)

# Webdriver
driver = webdriver.Chrome("/home/stefan/Knowledge/Bachelor-thesis/chromedriver")
driver.get(TWITTER_START_PAGE)

# Logging in
username_field = WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "input[name='session[username_or_email]']")
    )
)
password_field = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='session[password]']"))
)
username_field.clear()
password_field.clear()

username_field.send_keys("s.schoerkmeier@gmx.at")
password_field.send_keys("!23Juli1996!")
sleep(0.5)

login_field_xpath = '//*[@class="css-18t94o4 css-1dbjc4n r-42olwf r-sdzlij r-1phboty r-rs99b7 r-1fz3rvf r-usiww2 r-19yznuf r-64el8z r-1ny4l3l r-1dye5f7 r-o7ynqc r-6416eg r-lrvibr"]'
WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, login_field_xpath))
).click()
sleep(next(ENTER_DATA_SLEEP))

# Load liption twitter page
driver.get(TWITTER_LIPTON_PAGE)

# Load followers page
followers_xpath = '//*[@class="css-4rbku5 css-18t94o4 css-901oao r-18jsvk2 r-1loqt21 r-37j5jr r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-qvutc0"]'
WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.XPATH, followers_xpath))
).click()
sleep(2)

# ----- Utility -----
def urls_of_posts_to_crawl(self) -> set:
    urls_of_users = set()
    is_post_limit_reached = False

    while True:
        self.scroll_down()
        page_height = self.driver.execute_script(PAGE_HEIGHT_SCRIPT)
        total_scrolled_height = self.driver.execute_script(TOTAL_SCROLLED_HEIGHT_SCRIPT)

        for user_url in self._urls_of_users():
            urls_of_users.add(user_url)
            if (

                len(urls_of_users) >= MAXIMAL_FOLLOWERS
            ):
                is_post_limit_reached = True
                break
        if page_height - 1 <= total_scrolled_height or is_post_limit_reached:
            break

    return urls_of_users

def _urls_of_users(self) -> list:
    urls_of_users = self.driver.find_elements_by_xpath('//*[@class="css-1dbjc4n r-1wbh5a2 r-dnmrzs"]/a')
    urls_of_users = [url_of_post.get_attribute("href") for url_of_post in urls_of_users]
    urls_of_users = list(set(urls_of_users))

def scroll_down(self):
    self.driver.execute_script(
        f"window.scrollBy(0, {next(SCROLL_LENGTH_ON_WEBSITE)});"
    )
    sleep(next(ENTER_DATA_SLEEP))


# ======================= User workbench ==============================
# Constants:
TWITTER_USER_PAGE = "https://twitter.com/login"


driver = webdriver.Chrome("/home/stefan/Knowledge/Bachelor-thesis/chromedriver")
driver.get(TWITTER_START_PAGE)