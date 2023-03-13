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
        self.client = MongoClient(url, connectTimeoutMS=500, socketTimeoutMS=500)
        try:
            # self.client.server_info()
            self.client.admin.command('ping')
        except:
            print("Server not available")

    def DisplayDBList(self):
        print(self.client.list_database_names())

    def CreateDB(self, dbName):
        self.DB = self.client[dbName]

    def InsertDocument(self, collection_name, dynamic_val):
        self.DB[collection_name].insert_one(dynamic_val)
