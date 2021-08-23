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
import utility


class InstagramCrawlerSpider(scrapy.Spider):
    name = "instagram_crawler"
    allowed_domains = ["instagram.com"]
    start_urls = ["http://instagram.com/"]

    def start_requests(self):
        self.driver = webdriver.Chrome(
            "/home/stefan/Knowledge/Bachelor-thesis/chromedriver"
        )
        self.driver.get("https://www.instagram.com/")

        accept_all_cookies = WebDriverWait(
            self.driver, utility.SECONDS_FOR_TIMEOUT
        ).until(EC.element_to_be_clickable((By.XPATH, '//button[text()="Accept All"]')))
        accept_all_cookies.click()  # TODO Ponder: Is this nice this way or just work with comments?

        username = WebDriverWait(self.driver, utility.SECONDS_FOR_TIMEOUT).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']"))
        )
        password = WebDriverWait(self.driver, utility.SECONDS_FOR_TIMEOUT).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']"))
        )
        username.clear()
        password.clear()
        username.send_keys("stefandovakin")
        password.send_keys("dragonborn123")
        sleep(utility.ENTER_DATA_SLEEP)

        WebDriverWait(self.driver, utility.SECONDS_FOR_TIMEOUT).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        ).click()
        sleep(utility.CLICK_SLEEP)

        WebDriverWait(self.driver, utility.SECONDS_FOR_TIMEOUT).until(
            EC.element_to_be_clickable(
                (By.XPATH, '//button[contains(text(), "Not Now")]')
            )
        ).click()
        sleep(utility.CLICK_SLEEP)

        WebDriverWait(self.driver, utility.SECONDS_FOR_TIMEOUT).until(
            EC.element_to_be_clickable(
                (By.XPATH, '//button[contains(text(), "Not Now")]')
            )
        ).click()
        sleep(utility.CLICK_SLEEP)

        search_box = WebDriverWait(self.driver, utility.SECONDS_FOR_TIMEOUT).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Search']"))
        )
        search_box.clear()
        sleep(utility.CLICK_SLEEP)
        search_string = "marryicetea"
        search_box.send_keys(search_string)
        sleep(utility.ENTER_DATA_SLEEP)
        search_box.send_keys(Keys.ENTER)
        search_box.send_keys(Keys.ENTER)  # OR
        # search_box.send_keys("\n\n")
        sleep(utility.WAIT_FOR_RESPONSE_SLEEP)

        # self.driver.execute_script("window.scrollBy(0, 50);")  # Variable scrolling -> use for more organic scrolling
        self.driver.execute_script("window.scrollTo(0, 4000);")
        sleep(utility.ENTER_DATA_SLEEP)

        # images = self.driver.find_elements_by_tag_name("img")  # TODO Look this up in docu.
        image_urls = self.driver.find_elements_by_xpath("//a")
        image_urls = [image_url.get_attribute("href") for image_url in image_urls]

        cleaned_image_urls = [
            cleaned_url for cleaned_url in image_urls if "/p/" in cleaned_url
        ]

        # Scrap images and safe to csv
        writer = csv.writer(open("crawled_items.csv", "w"))
        writer.writerow(
            ["URL", "UID", "description", "hashtags", "likes", "people_liked_post"]
        )
        path = os.getcwd()
        path = os.path.join(path, "images_test")
        if not os.path.exists(path):
            os.mkdir(path)
        counter = 0

        for (
            image_container_url
        ) in cleaned_image_urls:  # TODO Ponder: Better name for image_container_url
            self.driver.get(image_container_url)
            sleep(utility.WAIT_FOR_RESPONSE_SLEEP)
            selector = Selector(text=self.driver.page_source)

            # TODO in scrapy here yield i guess
            UID = image_container_url.split("/p/")[1].split("/")[0]
            image_url = self.driver.find_elements_by_tag_name("img")[1].get_attribute(
                "src"
            )
            hashtags = self.driver.find_elements_by_xpath('//a[@class=" xil3i"]')
            hashtags = [hashtag.get_attribute("href") for hashtag in hashtags]
            description = selector.xpath(
                '//*[@class="C4VMK"]/span/text()'
            ).extract()  # TODO can we remove the dynamic values? -> also right now we only get the first paragraph
            likes = selector.xpath('//*[@class="zV_Nj"]/span/text()').extract_first()

            # people_liked_post_url = self.driver.find_elements_by_xpath('//a[@class="zV_Nj"]')[0].get_attribute("href")  # TODO Ask: why doesn't this work just out of intrest
            likes_box = self.driver.find_elements_by_xpath('//a[@class="zV_Nj"]')
            people_liked_post = set()
            counter = 0
            if len(likes_box) > 0:
                likes_box[0].click()
                sleep(utility.WAIT_FOR_RESPONSE_SLEEP)
                # TODO ponder, is it worth to get username or just href? search with username may be more organic? Or is it?
                while (
                    int(likes) > len(people_liked_post) and counter < 10
                ):  # TODO smart condition to end if we dont get all people
                    print("likes: ", likes)
                    print("people_liked_post: ", len(people_liked_post))
                    selector = Selector(text=self.driver.page_source)
                    temp_users = selector.xpath(
                        '//*[@class="FPmhX notranslate MBL3Z"]/text()'
                    ).extract()
                    # [people_liked_post.add(user) for user in temp_users] # TODO Ask: why this doesn't work?
                    for user in temp_users:
                        people_liked_post.add(user)

                    elements_inside_popup = self.driver.find_elements_by_xpath(
                        '//*[@class="FPmhX notranslate MBL3Z"]'
                    )
                    element_inside_popup = elements_inside_popup[
                        len(elements_inside_popup) - 1
                    ]
                    element_inside_popup.send_keys(Keys.DOWN * utility.SCROLL_LENGTH)
                    sleep(utility.CLICK_SLEEP)
                    counter += 1

            writer.writerow(
                [
                    image_container_url,
                    UID,
                    description,
                    hashtags,
                    likes,
                    people_liked_post,
                ]
            )
            save_as = os.path.join(path, "Marry - " + UID + ".jpg")
            wget.download(image_url, save_as)
            counter += 1

    def parse(self):
        pass

    def crawl_people(self):
        pass
