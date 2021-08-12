# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class InstagramScraperMarryItem(scrapy.Item):
    # define the fields for your item here:
    id_of_post = scrapy.Field()
    url_of_post = scrapy.Field()
    likes_of_post = scrapy.Field()
    hashtags_of_post = scrapy.Field()
    description_of_post = scrapy.Field()
    post_was_liked_by = scrapy.Field()
