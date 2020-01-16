import requests
import json
import sys

sys.path.append('./')

from storesync.items import StoreItem
from scrapy.loader import ItemLoader
from storesync.pipelines import StoresyncPipeline


url = 'https://www.romanspizza.co.za/api'

params = {"query":"{\n  stores {\n    id\n    lat\n    lng\n    halaal\n    name\n    address\n    area\n    phone\n    phoneTwo\n    phoneThree\n    phoneFour\n    isOnline\n    isAuraOnline\n    isTabletConnected\n    hasGenerator\n    hasDevice\n    externalId\n    day_0\n    day_1\n    day_2\n    day_3\n    day_4\n    day_5\n    day_6\n    isOnTheGo\n    __typename\n  }\n}\n","operationName":None}
headers = {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}

response = requests.post(url, headers=headers, json=params)

data = response.json()

for store in data['data']['stores']:
    loader = ItemLoader(item=StoreItem())
    loader.add_value('u_id', store['id'])
    loader.add_value('latitude', store['lat'])
    loader.add_value('longitude', store['lng'])
    loader.add_value('address', store['address'])
    loader.add_value('number', store['phone'])
    loader.add_value('brandName', store['name'])
    print(loader.load_item())