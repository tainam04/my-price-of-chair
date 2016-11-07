import uuid

from src.common.database import Database
import src.models.stores.constants as StoreConstants
import src.models.stores.errors as StoreErrors


class Store(object):
    def __init__(self, name, url_prefix, tag_name, query, _id = None):
        self.name = name
        self.url_prefix = url_prefix
        self.tag_name = tag_name
        self.query = query
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<Store {}>".format(self.name)


    def jason(self):
        return {
            "_id": self._id,
            "name": self.name,
            "url_prefix" : self.url_prefix,
            "tag_name" : self.tag_name,
            "query" : self.query
        }

    def save_to_mongo(self):
        Database.update(StoreConstants.COLLECTION, {"_id": self._id}, self.jason())

    @classmethod
    def get_by_id(cls, id):
        return cls(**Database.find_one(StoreConstants.COLLECTION, {"_id" : id}))


    @classmethod
    def get_by_name(cls, store_name):
        return cls(**Database.find_one(StoreConstants.COLLECTION, {"name": store_name}))


    @classmethod
    def get_by_url_prefix(cls, url_prefix):
        print(url_prefix)
        return cls(**Database.find_one(StoreConstants.COLLECTION, {"url_prefix": {"$regex":'^{}'.format(url_prefix)}}))
        #print( '^{}'.format(url_prefix))
        #return cls(**Database.find_one(StoreConstants.COLLECTION, {"url_prefix": {"$regex":"^{}$".format(url_prefix)}}))


    @classmethod
    def get_by_url(cls, url):
        store = None
        for i in range(0, len(url) + 1):
            try:
                store = cls(**Database.find_one(StoreConstants.COLLECTION, {"url_prefix": {"$regex":'^{}$'.format(url[:i])}}))
            except:
                store = None
                # raise StoreErrors.StoreNotFoundException("The URL Prefix used to find the store didn't give us any results.")
            if store is not None :
                return store

        raise StoreErrors.StoreNotFoundException("The URL Prefix used to find the store didn't give us any results.")

    @classmethod
    def all(cls):
        return [cls(**elem) for elem in Database.find(StoreConstants.COLLECTION, {})]

    def delete(self):
        Database.remove(StoreConstants.COLLECTION, {'_id' : self._id})