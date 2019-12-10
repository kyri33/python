# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from storesync.models import add_store

class StoresyncPipeline(object):
    def process_item(self, item, spider):

        add_store(dict(item))

        return item
