import scrapy
from cs_spider.items import CsSpiderItem
from urllib.parse import urljoin
import re


class TiebaSpider(scrapy.Spider):
    name = "tieba"
    allowed_domains = ["baidu.com"]
    start_urls = ["https://tieba.baidu.com/f?ie=utf-8&kw=csgo&pn=0"]

    def parse(self, response):

    def parse_detail(self, response):
        
