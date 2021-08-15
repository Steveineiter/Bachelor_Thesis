#!/bin/bash
row_entry=$(sed -n 2p users_to_crawl.csv)
while [ "$row_entry" ]; do
  IFS=, read -r username is_a_company is_a_deep_crawl <<<"$row_entry"
  echo "Working on $username, is a company: $is_a_company, is a deep crawl: $is_a_deep_crawl."

  cd /home/stefan/Knowledge/Bachelor-thesis/instagram_scraper/instagram_scraper || exit
  sleep 2
  scrapy crawl instagram_crawler -a username="$username" -a is_a_company="$is_a_company" -a is_a_deep_crawl="$is_a_deep_crawl"

  cd /home/stefan/Knowledge/Bachelor-thesis/instagram_scraper || exit
  sed -i 2d users_to_crawl.csv
  row_entry=$(sed -n 2p users_to_crawl.csv)
done

# ======================= Experimenting =======================
#echo "auch # kein Kommentar innerhalb" # , wohl aber außerhalb

#while IFS=, read -r field1 field2 field3
#do
#    echo "$field1 and $field2 and then $field3"
#done < users_to_crawl.csv

#sed -i 2d users_to_crawl.csv

#sed -n 2d users_to_crawl.csv

#FOO=$(sed -n 2p users_to_crawl.csv)
#
#while [ "$FOO" ]
#do
#  IFS=, read var1 var2 var3 <<< "$FOO"
#  echo "$FOO"
#  echo $var1
#  echo $var2
#  echo $var3
#  sed -i 2d users_to_crawl.csv
#  FOO=$(sed -n 2p users_to_crawl.csv)
#  sleep 5
#done
#
#echo "donezo"
# Pseudo code:
#  while foo != empty:
#    foo = $(sed -n 2p users_to_crawl.csv)
#    username, is_a_company, is_a_deep_crawl = foo
#    scrapy crawl arguments = foo
#    sed -i 2d users_to_crawl.csv
