import requests
import json
import sys
import os
import re

sys.path.append("./")

from storesync.items import StoreItem
from scrapy.loader import ItemLoader
from storesync.pipelines import StoresyncPipeline

url = 'http://www.mochachos.com/wp-json/wpgmza/v1/datatables/'

params_raw = "columns[0][data]:0\n\
columns[0][name]:\n\
columns[0][searchable]:true\n\
columns[0][orderable]:true\n\
columns[0][search][value]:\n\
columns[0][search][regex]:false\n\
columns[1][data]:1\n\
columns[1][name]:\n\
columns[1][searchable]:true\n\
columns[1][orderable]:true\n\
columns[1][search][value]:\n\
columns[1][search][regex]:false\n\
columns[2][data]:2\n\
columns[2][name]:\n\
columns[2][searchable]:true\n\
columns[2][orderable]:true\n\
columns[2][search][value]:\n\
columns[2][search][regex]:false\n\
columns[3][data]:3\n\
columns[3][name]:\n\
columns[3][searchable]:true\n\
columns[3][orderable]:true\n\
columns[3][search][value]:\n\
columns[3][search][regex]:false\n\
order[0][column]:1\n\
order[0][dir]:asc\n\
start:0\n\
length:1000\n\
search[value]:\n\
search[regex]:false\n\
phpClass:WPGMZA\MarkerListing\AdvancedTable\n\
map_id:1"

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'X-Requested-With': 'XMLHttpRequest',
            'X-WPGMZA-Action-Nonce': 'a7911ee7e0',
            'X-WP-Nonce': 'de903876a3'}
params = {}

for param in params_raw.split('\n'):
    key, value = param.split(':')[0:2]
    params[key] = value

response = requests.post(url, data=params, headers=headers)

if not response:
    # TODO ERROR
    exit(2)

js = json.loads(response.content)

for store in js['meta']:
    if store['category'] != 'Mochachos':
        continue
    brandName = store['title']
    raw = store['description']
    number = re.search('(\d+\)*(&nbsp;)*(</strong>)*-*\s*)+',raw)
    number = number.group()
    #add_raw = raw.split("<br />")
    #address = add_raw[-1][:add_raw[-1].index('</p>')]
    #print(address)
    add_raw = raw[raw.index('Address:') + 7:]
    address = re.search('>(.)*<', add_raw)
    print(address.group())
