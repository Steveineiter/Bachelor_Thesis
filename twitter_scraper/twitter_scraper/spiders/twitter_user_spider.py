import csv
import os
from time import sleep

import scrapy
from selenium import webdriver

from ..constants import *



class TwitterUserSpiderSpider(scrapy.Spider):
    name = 'twitter_user_spider'
    allowed_domains = ['twitter.com']
    start_urls = ['http://twitter.com/']

    def __init__(self):
        self.working_directory = os.getcwd()
        webdriver_path = os.path.join(self.working_directory, os.pardir, "chromedriver")
        self.driver = webdriver.Chrome(webdriver_path)

    def start_requests(self):
        user_urls = list()
        counter = 1
        with open(
                "/home/stefan/Knowledge/Bachelor-thesis/twitter_scraper/twitter_scraper/items/twitter_usernames_and_urls.csv",
                "r", newline=""
        ) as twitter_usernames_and_urls_csv_file:
            dict_reader = csv.DictReader(twitter_usernames_and_urls_csv_file)
            for row in dict_reader:
                url = row["url"]
                user_urls.append(url)
                if counter >= 5:
                    break
                counter += 1

        for url_of_user in user_urls:
            print("=" * 30)
            print(" Now Crawling")
            print(url_of_user)
            print("=" * 30, "\n")
            yield self.parse_profile(url_of_user)

    def parse_profile(self, url_of_user):
        self._load_web_site(url_of_user)


    def _load_web_site(self, url):
        self.driver.get(url)
        sleep(next(WAIT_FOR_RESPONSE_SLEEP))


