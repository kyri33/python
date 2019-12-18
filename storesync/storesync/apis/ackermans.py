import requests
import json
import sys
import os

sys.path.append("./")

from storesync.items import StoreItem
from scrapy.loader import ItemLoader
from storesync.pipelines import StoresyncPipeline


url = 'https://newprofile.ackermans.co.za/stores/NearbyStores/Ackermans/-26.2707593/28.112267900000006/2000000?tracker=qd8zeueued-1553755991-1'

response = requests.get(url)

if not response:
    # TODO ERROR
    exit(2)

results = json.loads(response.content)

posts = []
items = []
for store in results['stores']:

    loader = ItemLoader(item=StoreItem())
    loader.add_value('u_id', store['branch_id'])
    loader.add_value('address', store['address'])
    loader.add_value('brandName', store['description'])
    loader.add_value('number', store['telephone_number'])
    loader.add_value('latitude', store['latitude'])
    loader.add_value('longitude', store['longitude'])

    items.append(loader)

pipeline = StoresyncPipeline()
for item in items:
    pipeline.process_item(item.load_item(), None)