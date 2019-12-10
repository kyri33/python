import requests
import json
import from storesync.items import parse_number


url = 'https://newprofile.ackermans.co.za/stores/NearbyStores/Ackermans/-26.2707593/28.112267900000006/2000000?tracker=qd8zeueued-1553755991-1'

response = requests.get(url)

if not response:
    # TODO ERROR
    exit(2)

results = json.loads(response.content)

posts = []

for store in results['stores']:
    post = {
        'u_id': store['branch_id'],
        'brandName': store['description'],
        'address': store['address'],
        'latitude': store['latitude'],
        'longitude': store['longitude'],
        'number': parse_number(store['telephone_number'])
    }
    posts.append(post)

print(posts)
print(len(posts))