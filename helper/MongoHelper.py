from pymongo import MongoClient


# 방법1 - URI
# mongodb_URI = "mongodb://localhost:27017/"
# client = MongoClient(mongodb_URI)

# 방법2 - HOST, PORT
# client = MongoClient(host='localhost', port=27017)

class MyMongoClient(object):
    def __init__(self,kdip):
        self.KDIP = kdip


    def ConnectMongoServer(self, url):
        self.client = MongoClient(url)

    def DisplayDBList(self):
        print(self.client.list_database_names())

