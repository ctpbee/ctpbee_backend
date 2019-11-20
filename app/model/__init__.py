from pymongo import MongoClient

client = MongoClient(host='120.79.8.150', port=27017)
db = client['ctp_bar']
