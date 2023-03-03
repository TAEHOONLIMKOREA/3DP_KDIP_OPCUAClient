from pymongo import MongoClient


# 방법1 - URI
# mongodb_URI = "mongodb://localhost:27017/"
# client = MongoClient(mongodb_URI)

# 방법2 - HOST, PORT
client = MongoClient(host='localhost', port=27017)

def DisplayDBList():
    print(client.list_database_names())