# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from storesync.items import StoreItem


class SausagesaloonSpider(scrapy.Spider):
    name = 'sausagesaloon'
    allowed_domains = ['sausagesaloon.co.za']
    start_urls = ['https://sausagesaloon.co.za/store-locations/']

    def parse(self, response):
        for marker in response.css('div.marker'):
            loader = ItemLoader(item=StoreItem(), selector=marker)
            loader.add_css('brandName', 'h4::text')
            loader.add_css('latitude', '::attr(data-lat)')
            loader.add_css('longitude', '::attr(data-lng)')
            loader.add_css('address', 'p.address::text')
            loader.add_value('u_id', marker.css('h4::text').get())
            yield response.follow(marker.css('a')[0], callback=self.parse_store, meta={'store_item': loader.load_item()})
            
    def parse_store(self, response):
        store_item = response.meta['store_item']
        loader = ItemLoader(item=store_item, selector = response)
        number = response.css('div.contact-block').css('div')[1].css('a::text').get()
        loader.add_value('number', number)
        print(loader.load_item())