# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from storesync.items import StoreItem
from storesync.getcoordinates import get_coordinates


class AdegaSpider(scrapy.Spider):
    name = 'adega'
    allowed_domains = ['adegas.co.za']
    start_urls = ['https://www.adegas.co.za/branches/']

    def parse(self, response):
        items = response.css('div.pos-top')

        for item in items:
            loader = ItemLoader(item=StoreItem())
            brandName = item.css('h3::text').get()
            if brandName == None:
                continue
            loader.add_value('brandName', brandName)
            details = item.css('p::text').getall()
            number = details[0].split('/')[0]
            loader.add_value('number', number)
            address = details[3]
            loader.add_value('address', address)
            coords = get_coordinates(address)
            loader.add_value('latitude', coords['latitude'])
            loader.add_value('longitude', coords['longitude'])
            loader.add_value('u_id', brandName)
            print(loader.load_item())