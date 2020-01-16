# -*- coding: utf-8 -*-
import scrapy
from storesync.items import StoreItem
from scrapy.loader import ItemLoader
from storesync.getcoordinates import get_coordinates


class ColcacchioSpider(scrapy.Spider):
    name = 'colcacchio'
    allowed_domains = ['colcacchio.co.za']
    start_urls = ['https://colcacchio.co.za/locations/']

    def parse(self, response):
        
        for store in response.css('div.wpb_text_column'):
            loader = ItemLoader(item=StoreItem())
            brandName = store.css('h4::text').get()
            
            if brandName == None:
                brandName = store.css('h4').css('strong::text').get()
            
            if brandName == None or len(brandName) < 2:
                continue

            address = ''
            number = '0'
            meta = store.css('p::text').getall()
            for met in meta:
                digit = 0
                for i in met:
                    if i.isnumeric():
                        digit += 1
                if digit < 9 and '@' not in met and 'H00' not in met:
                    address += met
                elif digit > 9:
                    number = met
            
            address = address.replace('\n', ' ').strip()
            
            loader.add_value('brandName', brandName)
            loader.add_value('number', number)
            loader.add_value('address', address)
            coords = get_coordinates(address)
            latitude = coords['latitude']
            longitude = coords['longitude']
            loader.add_value('latitude', latitude)
            loader.add_value('longitude', longitude)
            print(loader.load_item())