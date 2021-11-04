# Bachelor-thesis documentation

## Table of contents
1. Overview
2. Instagram Scraper
   1. Important Files and Directories
   2. How to install and run it
3. Twitter Scraper
   1. Important Files and Directories
   2. How to install and run it


## 1.) Overview
This documentation is focused on the Crawling part of the Bachelor-thesis. Other areas like machine learning and data 
representation are treated separately with Jupyter notebooks.  

There are two different crawlers: 
- A instagram crawler using scrapy and selenium.
- A twitter crawler using scrapy and selenium as well for getting usernames and a scweet_crawler for 
getting details out of those profiles.

Data management has been archived via CSV files.

## 2.) Instagram Scraper
This crawler is using scrapy and selenium. It is used for all purposes:
- Crawling a company.
- Crawling a user / consumer.
- Crawling for shallow data: Things we can get from the profile: Description, # Followers, # Following...
- Crawling for deep data: Things we can get from the profile (with more depth, eg. names of Followers / Following) and information we can get from posts: The image, descriptions, # of likes, who liked it...

This is set via the parameters ```is_a_company``` and ```is_a_deep_crawl```.

The parameter ```user_count_to_load_from_csv```is used to load x user which we would like to crawl from a given csv file. As an example refer to the file instagram_scraper/users_to_crawl.csv.

The parameter ```is_raspberry_pi``` is used if we wish to crawl from a raspberry pi, since it needs a different version of the chromium-browser chromedriver.

### 2.i) Important Files and Directories
In the directory instagram_scraper/instagram_scraper:  
- spiders/instagram_crawler.py:
  - This file contains the crawler for Instagram. It handles the request and parsing part of the crawler.
- constants.py
  - This file is the most important to tune parameters: Eg. wait time between requests, scrolling distance, profiles to log in with.
- csv_handler.py
- file_manager.py
  - Handles everything in the file system except CSV files. 

The other files, including items.py, middlewares.py, pipelines.py and settings.py, belong to the standard scrapy files. Please refer to https://docs.scrapy.org/en/latest/ for further information.

The directory instagram_scraper/items contains all the crawled data. The **companies** directory contains all the relevant data of the client and the **consumers** directory all the relevant data about the consumers.

The shell-scripts **crawl_users_from_csv.sh** and **crawl_users_from_csv_with_raspberry.sh** are a simple way to execute the crawler. 

### 2.ii) How to install and run it
Install scrapy, selenium and the chromedriver.
You maybe need to adapt the chromedriver path in the ```__init__``` function in the InstagramSpider.

You can either run the **crawl_users_from_csv.sh** script or to run it in Pycharm get configurations like this: 
![image](https://user-images.githubusercontent.com/53307237/129472345-02f5f040-1ee5-4eef-af74-6181e8f059bf.png)

To run it in Pycharm with arguments:
![image](https://user-images.githubusercontent.com/53307237/129472352-99c67a38-3634-46cd-bbb8-0287847615c1.png)

Arguments can be:
- username: The Username we want to scrape.
- is_a_company: True if the user we scrape is a company, where we want to get data, like Marry or Makava. False otherwise.
- is_a_deep_crawl: True if we want to crawl data from posts, not only the profile. Needs MUCH longer if set on True.
- path_to_useres_to_crawl_csv: If we use a CSV and the bash script for automatically scarping users, you need to pass the absolute path as argument so that the csv gets updatet after each scrape.



## 3.) Twitter Scraper
This crawler using scrapy and selenium to get usernames / profiles and a scweet_crawler for 
getting details out of those profiles.

### 3.i) Important Files and Directories
In the directory twitter_scraper/twitter_scraper:  
- spiders/twitter_followers_spider.py:
    - this file contains the crawler to get the usernames of Twitter users. 
    - You have to set the target Twitter side as well as your Username and the Password in **constants.py** 
    - This is required to log in to Twitter, so it can search for user names in the followers section.
- constants.py:
  - This file is the most important to tune parameters: Eg. change the company to crawl, change the username / password to log in.

The other files, including items.py, middlewares.py, pipelines.py and settings.py, belong to the standard scrapy files. Please refer to https://docs.scrapy.org/en/latest/ for further information.

The file twitter_scraper/scweet_crawler/scweetCrawler.py includes a simple implementation that reads usernames from a csv file and then crawls for them using scweet. Please refer to https://github.com/Altimis/Scweet for further information.


### 3.ii) How to install and run it
Install scrapy, selenium, chromedriver and the scweet_crawler. 

The process to use the twitter_followers_spider is analogue to that of the Instagram spider. 

To run it in Pycharm with arguments:

![Screenshot from 2021-11-04 15-49-35](https://user-images.githubusercontent.com/53307237/140335992-1779b723-1d10-4286-9e3f-f4c108a7bd55.png)

To run the scweet_crawler just execute the **scweetCrawler.py** file as any other python program.
