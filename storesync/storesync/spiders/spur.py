# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import FormRequest
from storesync.items import StoreItem
from scrapy.loader import ItemLoader


class SpurSpider(scrapy.Spider):
    name = 'spur'
    allowed_domains = ['spur.co.za']
    start_urls = ['https://www.spur.co.za/find-a-spur/']

    def parse(self, response):
        cookie = response.headers.getlist("Set-Cookie")[0]
        csrf = response.css('form#__AntiForgeryForm').css('input::attr(value)').get()
        ufprt = response.css('input[name="ufprt"]::attr(value)').get()
        frmdata = {
            '__RequestVerificationToken': csrf,
            'Province': '',
            'Provinceinput': '',
            'City': '',
            'Cityinput': '',
            'Suburb': '',
            'Suburbinput': '',
            'KeywordSearch': '',
            'Generator': 'false',
            'WirelessAccess': 'false',
            'DisabledFacilities': 'false',
            'SmokingArea': 'false',
            'Halaal': 'false',
            'ufprt': ufprt
        }
        url = 'https://www.spur.co.za/find-a-spur/'

        return FormRequest(url, formdata=frmdata, 
                headers={'Cookie': cookie}, callback=self.parse_stores,
                method='POST')

    def parse_stores(self, response):
        
        for store in response.css('div.locator-result'):
            loader = ItemLoader(item=StoreItem())
            brandName = store.css('h4::text').get().replace(' Spur', '')
            number = store.css('strong[itemprop="telephone"]::text').get()
            address = store.css('p[itemprop="address"]::text').get()
            latitude = store.css('meta[itemprop="latitude"]::attr(content)').get()
            longitude = store.css('meta[itemprop="longitude"]::attr(content)').get()

            loader.add_value('brandName', brandName)
            loader.add_value('number', number)
            loader.add_value('address', address)
            loader.add_value('latitude', latitude)
            loader.add_value('longitude', longitude)
            print(loader.load_item())