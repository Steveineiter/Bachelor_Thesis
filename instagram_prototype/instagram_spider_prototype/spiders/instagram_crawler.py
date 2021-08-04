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

        username = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']")))
        password = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']")))
        username.clear()
        password.clear()
        username.send_keys("stefandovakin")
        password.send_keys("dragonborn123")
        sleep(2)

        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()
        sleep(1)

        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Not Now")]'))).click()
        sleep(2)

        search_box = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Search']")))
        search_box.clear()
        sleep(.5)
        search_string = "marryicetea"
        search_box.send_keys(search_string)
        sleep(1)
        search_box.send_keys(Keys.ENTER)
        search_box.send_keys(Keys.ENTER)  # OR
        # search_box.send_keys("\n\n")
        sleep(5)

        # self.driver.execute_script("window.scrollBy(0, 50);")  # Variable scrolling -> use for more organic scrolling
        self.driver.execute_script("window.scrollTo(0, 4000);")
        sleep(1)

        # images = self.driver.find_elements_by_tag_name("img")  # TODO Look this up in docu.
        image_urls = self.driver.find_elements_by_xpath('//a')
        image_urls = [image_url.get_attribute("href") for image_url in image_urls]

        cleaned_image_urls = [cleaned_url for cleaned_url in image_urls if "/p/" in cleaned_url]

        # Scrap images and safe to csv
        writer = csv.writer(open("crawled_items.csv", "w"))
        writer.writerow(["description", "hashtags", "likes"])
        path = os.getcwd()
        path = os.path.join(path, "images_test")
        if not os.path.exists(path):
            os.mkdir(path)
        counter = 0


        for image_container_url in cleaned_image_urls:  # TODO Ponder: Better name for image_container_irl
            self.driver.get(image_container_url)
            sleep(5)
            selector = Selector(text=self.driver.page_source)  # TODO here should be a bug

            # TODO in scrapy here yield i guess
            image_url = self.driver.find_elements_by_tag_name("img")[1].get_attribute("src")
            hashtags = self.driver.find_elements_by_xpath('//a[@class=" xil3i"]')
            hashtags = [hashtag.get_attribute("href") for hashtag in hashtags]
            description = selector.xpath('//*[@class="C4VMK"]/span/text()').extract_first()  # TODO can we remove the dynamic values?
            likes = selector.xpath('//*[@class="zV_Nj"]/span/text()').extract_first()

            writer.writerow([description, hashtags, likes])
            save_as = os.path.join(path, "Image" + str(counter) + ".jpg")
            wget.download(image_url, save_as)
            counter += 1

    def parse(selfs):
        pass






