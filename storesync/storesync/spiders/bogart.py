# -*- coding: utf-8 -*-
import scrapy
from storesync.items import StoreItem
from scrapy.loader import ItemLoader

class BogartSpider(scrapy.Spider):
    name = 'bogart'
    allowed_domains = ['bogart.co.za']
    start_urls = ['https://www.bogart.co.za/pages/contact-us']

    def parse(self, response):
        container = response.css('div.rte')
        items = container.css('p')
        lastLoader = None
        for item in items:

            txts = item.css('::text')
            if len(txts) > 2:
                loader = ItemLoader(item=StoreItem())
                for sel in txts:
                    txt = sel.get()
                    if '___' in txt or txt == ' ':
                        continue

                    if 'Tel' in txt:
                        loader.add_value('number', txt[5:])
                    elif 'Address' in txt:
                        loader.add_value('address', txt[9:])
                    else:
                        loader.add_value('brandName', txt)
                        loader.add_value('u_id', txt)
                lastLoader = loader

            iframesrc = item.css('iframe::attr(src)').get()
            if iframesrc != None and lastLoader != None:
                six = iframesrc.index('!2d')
                eix = iframesrc.index('!3d')
                fix = iframesrc.index('!', eix + 3)
                longitude = iframesrc[six + 3 : eix]
                latitude = iframesrc[eix + 3 : fix]
                
                lastLoader.add_value('latitude', latitude)
                lastLoader.add_value('longitude', longitude)
                yield loader.load_item()