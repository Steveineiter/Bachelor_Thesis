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


class InstagramCrawlerSpider(scrapy.Spider):
    name = 'instagram_crawler'
    allowed_domains = ['instagram.com']
    start_urls = ['http://instagram.com/']

    def start_requests(self):
        self.driver = webdriver.Chrome(
            "/home/stefan/Knowledge/Bachelor-thesis/chromedriver"
        )
        self.driver.get("https://www.instagram.com/")

        accept_all_cookies = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[text()="Accept All"]'))
        )
        accept_all_cookies.click()  # TODO Ponder: Is this nice this way or just work with comments?
