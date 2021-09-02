# from twitterscraper import query_tweets
# from twitterscraper.query import query_tweets_from_user
# import pandas as pd
#
#
#
# user = 'realDonaldTrump'
# tweets = query_tweets_from_user(user, use_proxy=False)
# df = pd.DataFrame(t.__dict__ for t in tweets)
#
# df = df.loc[df['screen_name'] == user]
#
# df = df['text']
# =============================================================================================

# import re, requests
#
# headers = { 'User-Agent': 'UCWEB/2.0 (compatible; Googlebot/2.1; +google.com/bot.html)'}
#
#
# def cleanhtml(raw_html):
#   cleanr = re.compile('<.*?>')
#   cleantext = re.sub(cleanr, '', raw_html)
#   return cleantext
#
# content = ""
# for user in ['billgates']:
#     content += "============================\n\n"
#     content += user + "\n\n"
#     content += "============================\n\n"
#     url_twitter = 'https://twitter.com/%s' % user
#     resp = requests.get(url_twitter, headers=headers)  # Send request
#     res = re.findall(r'<p class="TweetTextSize.*?tweet-text.*?>(.*?)</p>',resp.text)
#     for x in res:
#         x = cleanhtml(x)
#         x = x.replace("&#39;","'")
#         x = x.replace('&quot;','"')
#         x = x.replace("&nbsp;"," ")
#         content += x
#         content += "\n\n"
#         content += "---"
#         content += "\n\n"
#
#     print(content)
# =============================================================================================
import csv

from Scweet.scweet import scrape
from Scweet.user import get_user_information, get_users_following, get_users_followers


# data = scrape(hashtag="bitcoin", since="2021-08-05", until=None, from_account = None, interval=1,
# 	headless=True, display_type="Top", save_images=False,
# 	resume=False, filter_replies=True, proximity=True)


users = set()
counter = 1
with open(
        "/home/stefan/Knowledge/Bachelor-thesis/twitter_scraper/twitter_scraper/items/twitter_usernames_and_urls.csv",
        "r", newline=""
) as twitter_usernames_and_urls_csv_file:
    dict_reader = csv.DictReader(twitter_usernames_and_urls_csv_file)
    for row in dict_reader:
        user = row["username"]
        users.add(user)
        if counter >= 10:
            break
        counter += 1


# data = get_user_information(users)
for user in users:
    print("\n\nNow scraping: ", user)
    data = scrape(from_account=user, since="2021-06-01", headless=False, interval=15)

# data = scrape(from_account="Kingrecs", since="2021-04-28", headless=False)

# env_path = ".env"
# users = ["lipton"]
#
# followers = get_users_followers(users=users, env=env_path, verbose=0, headless=True, wait=2, limit=50, file_path=None)
