import requests
import json
from scrapy import Selector
import sys

sys.path.append('./')

from storesync.items import StoreItem
from storesync import getcoordinates
from scrapy.loader import ItemLoader
from storesync.pipelines import StoresyncPipeline

url = 'https://www.primi-world.co.za/wp-admin/admin-ajax.php'

params = {'action': 'get_posts_from_cat1', 'dataType': 'json'}

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'}

response = requests.post(url, data=params, headers=headers)

if not response:
    # TODO ERROR
    exit(2)

js = json.loads(response.content)

for store in js['data'][1]:
    selector = Selector(text=store)
    brandName = selector.css('div.tab-title::text').get()
    address = ' '.join(selector.css('div.store-locator-tabdetail-left::text').getall()).strip()
    number = selector.css('store-locator-tabdetail-left').css('a::text').get()
    coords = getcoordinates.get_coordinates(address)
    loader = ItemLoader(item=StoreItem())
    loader.add_value('brandName', brandName)
    loader.add_value('address', address)
    loader.add_value('number', number)
    loader.add_value('latitude', coords['latitude'])
    loader.add_value('longitude', coords['longitude'])
    print(loader.load_item())