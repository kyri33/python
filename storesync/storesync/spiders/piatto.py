# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from storesync.items import StoreItem

class PiattoSpider(scrapy.Spider):
    name = 'piatto'
    allowed_domains = ['piatto.co.za', 'piatto.co.za.dedi152.jnb2.host-h.net']
    start_urls = ['https://www.piatto.co.za/stores/']

    def parse(self, response):
        
        for link in response.css('div.img').css('a'):
            yield response.follow(link, callback=self.parse_store)
    
    def parse_store(self, response):
        brandName = response.css('h1::text').get().replace('PIATTO', '').strip()
        address = ' '.join(response.css('div.medium-3')[0].css('p')[0].css('::text').getall())
        number = response.css('div.medium-3')[0].css('p')[1].css('::text').get()
        coords = response.css('iframe::attr(src)').get()
        longitude = coords[coords.index('!2d') + 3 : coords.index('!3d')]
        latitude = coords[coords.index('!3d') + 3 : coords.index('!2m')]
        u_id = brandName

        loader = ItemLoader(item=StoreItem())
        loader.add_value('brandName', brandName)
        loader.add_value('address', address)
        loader.add_value('number', number)
        loader.add_value('longitude', longitude)
        loader.add_value('latitude', latitude)
        loader.add_value('u_id', u_id)
        print(loader.load_item())