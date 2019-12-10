import pymongo

client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['mydb']

storeCol = db['stores']

def add_store(store):
    storeCol.insert_one(store)