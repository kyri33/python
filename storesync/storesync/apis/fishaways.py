import requests
import xml.etree.ElementTree as ET
import sys
import os

sys.path.append("./")

from storesync.items import StoreItem
from scrapy.loader import ItemLoader
from storesync.pipelines import StoresyncPipeline


url = 'http://locator.steers.co.za/SearchResponse.aspx?radius=100000&tag=All%20Steers&brandid=3'

def getaddress(addressLine, nospace=False):
    #print(addressLine)
    if addressLine != None:
        return ' ' + addressLine if not nospace else addressLine
    return ''
        

response = requests.get(url)

if not response:
    # TODO ERROR
    exit(2)

results = ET.fromstring(response.content)

for item in results.findall('marker'):
    u_id = item.get('lStoreId')
    brandName = item.get('sName')
    number = item.get('sTelNo')

    address = getaddress(item.get('Address1Line1'), nospace=True) + getaddress(item.get('Address1Line2'))
    address += getaddress(item.get('Address1Line3')) + getaddress(item.get('Address1Line4')) \
            + getaddress(item.get('Address1Line5'))

    latitude = item.get('Latitude')
    longitude = item.get('Longitude')

    loader = ItemLoader(item=StoreItem())
    loader.add_value('u_id', u_id)
    loader.add_value('brandName', brandName)
    loader.add_value('number', number)
    loader.add_value('latitude', latitude)
    loader.add_value('longitude', longitude)
    loader.add_value('address', address)

    print(loader.load_item())