# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CsSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    #标题
    title= scrapy.Field()
    #内容
    content= scrapy.Field()
    #链接
    link= scrapy.Field()
    #回复数
    reply_num= scrapy.Field()

    pass
