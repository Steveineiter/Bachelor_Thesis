# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


# Note: If you change something here, also change in constants file.
class ProfileDataItem(scrapy.Item):
    name_of_profile = scrapy.Field()
    number_of_posts = scrapy.Field()
    followers = scrapy.Field()
    following = scrapy.Field()
    description_of_profile = scrapy.Field()
    hashtags_of_description = scrapy.Field()
    other_tags_of_description = scrapy.Field()
    lifestyle_stories = scrapy.Field()  # TODO Ask: how is this really called?
    is_private = scrapy.Field()
    following_names = scrapy.Field()


class PostDataItem(scrapy.Item):
    # define the fields for your item here:
    id_of_post = scrapy.Field()
    url_of_post = scrapy.Field()
    likes_of_post = scrapy.Field()
    hashtags_of_post = scrapy.Field()
    description_of_post = scrapy.Field()
    post_was_liked_by = scrapy.Field()
    date_of_post = scrapy.Field()



