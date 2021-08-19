#!/bin/bash
row_entry=$(sed -n 2p users_to_crawl.csv)
while [ "$row_entry" ]; do
  IFS=, read -r username is_a_company is_a_deep_crawl <<<"$row_entry"
  echo
  echo "==================================================================================="
  echo "Working on '$username', is a company: '$is_a_company', is a deep crawl: '$is_a_deep_crawl'."
  echo "==================================================================================="
  echo

  cd /home/stefan/Knowledge/Bachelor-thesis/instagram_scraper/instagram_scraper || exit
  scrapy crawl instagram_crawler -a username="$username" -a is_a_company="$is_a_company" -a is_a_deep_crawl="$is_a_deep_crawl" -a path_to_users_to_crawl_csv="/home/stefan/Knowledge/Bachelor-thesis/instagram_scraper/users_to_crawl.csv"
  sleep 5

  cd /home/stefan/Knowledge/Bachelor-thesis/instagram_scraper || exit
  #  sed -i 2d users_to_crawl.csv  # Is now handled by file_manager.py
  row_entry=$(sed -n 2p users_to_crawl.csv)
done