# -*- coding: utf-8 -*-
import scrapy
import requests
from storesync import getcoordinates
from scrapy.loader import ItemLoader
from storesync.items import StoreItem

class MuggandbeanSpider(scrapy.Spider):
    name = 'muggandbean'
    allowed_domains = ['muggandbean.co.za']
    start_urls = ['https://location.muggandbean.co.za/index.html']

    def parse(self, response):
        for province in response.css('a.Directory-listLink'):
            yield response.follow(province, callback=self.parse_province)

    def parse_province(self, response):
        for area in response.css('a.Directory-listLink'):
            yield response.follow(area, callback=self.parse_area)

    def parse_area(self, response):
        for store in response.css('a.Teaser-titleLink'):
            yield response.follow(store, callback=self.parse_store)

    def parse_store(self, response):
        brandName = response.css('span.LocationName-geo::text').get()
        number = response.css('div.phone-main::text').get()
        core_address = response.css('div.Core-address')
        address = core_address.css('div.c-AddressRow').css('span::text').getall()
        address = ' '.join(address)
        coords = getcoordinates.get_coordinates(address)

        loader = ItemLoader(item=StoreItem())
        loader.add_value('brandName', brandName)
        loader.add_value('number', number)
        loader.add_value('address', address)
        loader.add_value('latitude', coords['latitude'])
        loader.add_value('longitude', coords['longitude'])
        print(loader.load_item())