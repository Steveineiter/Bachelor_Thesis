# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class InstagramScraperMarryItem(scrapy.Item):
    # define the fields for your item here:
    post_id = scrapy.Field()
    url_of_post = scrapy.Field()

    # TODO get those later
    # description = scrapy.Field()
    # hashtags = scrapy.Field()
    #
    # likes = scrapy.Field()
    # people_liked_post = scrapy.Field()



