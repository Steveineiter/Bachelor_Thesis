# Selenium imports
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

driver = webdriver.Chrome("/home/stefan/Knowledge/Bachelor-thesis/chromedriver")
driver.get("http://instagram.com/")

WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[text()="Accept All"]'))).click()  # TODO Ponder: Is this nice this way or just work with comments?

username = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']")))
password = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']")))
username.clear()
password.clear()
username.send_keys("stefandovakin")
password.send_keys("dragonborn123")
sleep(0.5)

WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()

WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Not Now")]'))).click()

search_box = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Search']")))
search_box.clear()
sleep(.5)
search_string = "marryicetea"
search_box.send_keys(search_string)
sleep(1)
search_box.send_keys(Keys.ENTER)
search_box.send_keys(Keys.ENTER) # OR 
# search_box.send_keys("\n\n")

# driver.execute_script("window.scrollBy(0, 50);")  # Variable scrolling -> use for more organic scrolling
driver.execute_script("window.scrollTo(0, 4000);")

# images = driver.find_elements_by_tag_name("img")  # TODO Look this up in docu.
image_urls = driver.find_elements_by_xpath('//a')
image_urls = [image_url.get_attribute("href") for image_url in image_urls]

cleaned_image_urls = [cleaned_url for cleaned_url in image_urls if "/p/" in cleaned_url]

# Scrap images and safe to csv
selector = Selector(text=driver.page_source)

for image_container_url in cleaned_image_urls:  # TODO Ponder: Better name for image_container_irl
	driver.get(image_container_url)

	# TODO in scrapy here yield i guess
	image = driver.find_elements_by_tag_name("img")[1].get_attribute("src")
	hashtags =  driver.find_elements_by_xpath('//a[@class=" xil3i"]')
	hashtags = [hashtag.get_attribute("href") for hashtag in hashtags]
	description = selector.xpath('//*[@class="C4VMK"]/span/text()').extract_first()










