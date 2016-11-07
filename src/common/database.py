
import pymongo

class Database(object) :
    URI = "mongodb://127.0.0.1:27017"
    DATABASE_NAME="fullstack"
    DATABASE = None


    @staticmethod
    def initialize():
        client = pymongo.MongoClient(Database.URI)
        Database.DATABASE = client[Database.DATABASE_NAME]

    @staticmethod
    def insert(collection, data):
        Database.DATABASE[collection].insert(data)

    @staticmethod
    def update(collection, query, data):
        Database.DATABASE[collection].update(query, data, upsert=True)

    @staticmethod
    def remove(collection, query):
        Database.DATABASE[collection].remove(query)

    @staticmethod
    def find(collection, query):
        return Database.DATABASE[collection].find(query)


    @staticmethod
    def find_one(collection, query):
        return Database.DATABASE[collection].find_one(query)
