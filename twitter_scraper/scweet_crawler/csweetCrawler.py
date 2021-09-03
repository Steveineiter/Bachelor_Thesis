import csv

from Scweet.scweet import scrape
import pandas as pd

# Constatns:
USERNAMES_CSV_FILE = "/home/stefan/Knowledge/Bachelor-thesis/twitter_scraper/scweet_crawler/twitter_usernames_and_urls.csv"


def delete_row_from_twitter_usernames_and_urls_csv(path_to_users_to_crawl_csv):
    data_frame = pd.read_csv(path_to_users_to_crawl_csv)
    data_frame = data_frame.iloc[1:]
    data_frame.to_csv(path_to_users_to_crawl_csv, index=False)


users = list()
counter = 1
with open(
        USERNAMES_CSV_FILE,
        "r", newline=""
) as twitter_usernames_and_urls_csv_file:
    dict_reader = csv.DictReader(twitter_usernames_and_urls_csv_file)
    for row in dict_reader:
        user = row["username"]
        users.append(user)

for user in users:
    print("\n\nNow scraping: ", user)
    data = scrape(from_account=user, since="2021-01-01", headless=True, interval=30)
    delete_row_from_twitter_usernames_and_urls_csv(USERNAMES_CSV_FILE)

