# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from storesync.items import StoreItem


class PizzadelfornoSpider(scrapy.Spider):
    name = 'pizzadelforno'
    allowed_domains = ['delforno.co.za']
    start_urls = ['https://www.delforno.co.za/our-stores.html']

    def parse(self, response):
        for item in response.css('div.food-menu2-box'):
            yield response.follow(item.css('a')[0], callback=self.parse_store)

    def parse_store(self, response):
        brandName = response.css('h2.title-bar-medium-left::text').get().replace('Del Forno', '').strip()
        info = response.css('div.contact-us-left').css('li')[0]
        address = info.css('p::text').get()
        coords = info.css('p')[1].css('::text').get()
        latitude = coords[coords.index('-') : coords.index('|')].strip()
        longitude = coords[coords.index('|') + 1 : ].strip()
        number = response.css('a.my_call::text').get()
        u_id = brandName

        loader = ItemLoader(item=StoreItem())
        loader.add_value('brandName', brandName)
        loader.add_value('address', address)
        loader.add_value('number', number)
        loader.add_value('u_id', u_id)
        loader.add_value('latitude', latitude)
        loader.add_value('longitude', longitude)
        print(loader.load_item())
