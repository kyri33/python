# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field
from scrapy.loader.processors import MapCompose, TakeFirst

def parse_number(number):
    number = number.replace(' ', '')
    number = number.replace('(', '')
    number = number.replace(')', '')
    number = number.replace('+', '')
    return number

class StoresyncItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class StoreItem(scrapy.Item):
    brandName = Field(
        input_processor = MapCompose(str.strip),
        output_processor=TakeFirst()
    )
    number = Field(
        input_processor = MapCompose(parse_number),
        output_processor = TakeFirst()
    )
    address = Field(
        input_processor = MapCompose(str.strip),
        output_processor = TakeFirst()
    )
    u_id = Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )
    latitude = Field(
        input_processor = MapCompose(str.strip),
        output_processor = TakeFirst()
    )
    longitude = Field(
        input_processor = MapCompose(str.strip),
        output_processor = TakeFirst()
    )