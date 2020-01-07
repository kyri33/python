import requests
import json
import sys
import os

sys.path.append("./")

from storesync.items import StoreItem
from scrapy.loader import ItemLoader
from storesync.pipelines import StoresyncPipeline

url = "https://oceanbasket.com/dev/site/ajaxgetbranches?site_id=1&ignore=true"

response = requests.post(url)
if not response:
    print("Error")
    exit(2)

results = json.loads(response.content)

posts = []
items = []

for store in results['branches']:
    loader = ItemLoader(item=StoreItem())
    loader.add_value('u_id', store['id'])
    loader.add_value('address', store['meta_address'])
    loader.add_value('number', store['meta_phone'])
    loader.add_value('latitude', store['meta_latitude'])
    loader.add_value('longitude', store['meta_longitude'])
    loader.add_value('brandName', store['meta_title'])
    # TODO CAN FILTER PROVINCES
    print(loader.load_item())