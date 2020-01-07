# -*- coding: utf-8 -*-
import scrapy
import json
from storesync.items import StoreItem
from scrapy.loader import ItemLoader


class JohndorysSpider(scrapy.Spider):
    name = 'johndorys'
    allowed_domains = ['https://www.johndorys.co.za']
    start_urls = ['https://www.johndorys.co.za/find-a-restaurant/?ParentId=1300&Results=true']

    def parse(self, response):

        js = response.css('div.content').css('script::text').get()
        data = js[js.index('[{') :]
        data = data[0: data.index("}]'") + 2]
        
        results = json.loads(data)
        for store in results:
            loader = ItemLoader(item=StoreItem())
            brandName = store['DisplayName'].replace("John Dory's ", '')
            number = store['TelephoneNumber']
            address = store['StreetAddress'] + " " + store['Suburb'] + " " + store['City']
            latitude = store['Latitude']
            longitude = store['Longitude']
            u_id = brandName

            loader.add_value('u_id', u_id)
            loader.add_value('address', address)
            loader.add_value('brandName', brandName)
            loader.add_value('number', number)
            loader.add_value('latitude', latitude)
            loader.add_value('longitude', longitude)