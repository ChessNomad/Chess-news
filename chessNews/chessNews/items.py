# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ChessnewsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    date = scrapy.Field()
    author = scrapy.Field()
    country = scrapy.Field()
    comment_count = scrapy.Field()
    category = scrapy.Field()
    img_title = scrapy.Field()

