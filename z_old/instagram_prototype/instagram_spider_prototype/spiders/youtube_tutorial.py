# Selenium imports
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

# Other imports
import os
import wget

import scrapy
from time import sleep


class YoutubeTutorialSpider(scrapy.Spider):
    name = "youtube_tutorial"
    allowed_domains = ["instagram.com"]
    start_urls = ["http://instagram.com/"]

    def start_requests(self):
        self.driver = webdriver.Chrome(
            "/home/stefan/Knowledge/Bachelor-thesis/chromedriver"
        )
        self.driver.get("https://www.instagram.com/")

        # Since selenium does not support text evaluation we need XPATH here.
        accept_all_cookies = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[text()="Accept All"]'))
        )
        accept_all_cookies.click()  # TODO Ponder: Is this nice this way or just work with comments?

        username = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']"))
        )
        password = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']"))
        )
        username.clear()
        password.clear()
        username.send_keys("stefandovakin")
        password.send_keys("dragonborn123")

        log_in = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        )
        log_in.click()

        safe_login_info_not_now = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Not Now")]'))
        )
        safe_login_info_not_now.click() # TODO Ponder: Is this nice this way or just work with comments?

        turn_on_notification_not_now = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Not Now")]'))
        )
        turn_on_notification_not_now.click() # TODO Ponder: Is this nice this way or just work with comments?

        search_box = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Search']"))
        )
        search_box.clear()
        keyword = "#cat"
        search_box.send_keys(keyword)
        sleep(1)
        search_box.send_keys(Keys.ENTER)
        search_box.send_keys(Keys.ENTER)
        sleep(6)

        self.driver.execute_script("window.scrollTo(0, 4000);")
        images = self.driver.find_elements_by_tag_name("img")
        self.log(images)
        images = [image.get_attribute("src") for image in images]
        self.log(images)


        # Save images to computer.
        path = os.getcwd()
        path = os.path.join(path, keyword[1:] + "s")

        os.mkdir(path)

        counter = 0
        for image in images:
            save_as = os.path.join(path, keyword[1:] + str(counter) + ".jpg")
            wget.download(image, save_as)
            counter += 1

        sleep(5)

    def parse(self, response):
        pass
