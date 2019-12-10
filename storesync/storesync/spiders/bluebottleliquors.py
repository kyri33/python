# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from storesync.items import StoreItem

class BluebottleliquorsSpider(scrapy.Spider):
    name = 'bluebottleliquors'
    allowed_domains = ['bluebottleliquors.co.za']
    start_urls = ['http://bluebottleliquors.co.za/Stores']

    def parse(self, response):
        container = response.css('div.resp-tabs-container div.resp_container')[2]
        items = container.css('div.row')
        for item in items:
            loader = ItemLoader(item=StoreItem(), selector = item)
            loader.add_css('brandName', 'h1::text')
            yield loader.load_item()