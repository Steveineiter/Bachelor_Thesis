#!/bin/bash
scrapy crawl instagram_crawler -a is_a_company=False -a is_a_deep_crawl="True" -a user_count_to_load_from_csv=5 -a path_to_users_to_crawl_csv="/home/pi/Knowledge/Bachelor-thesis/instagram_scraper/users_to_crawl.csv" -a is_raspberry_pi=True