import pymongo
from bson.objectid import ObjectId

#pymongo tutorial: http://api.mongodb.com/python/current/tutorial.html
class MongoDBManager:
    def __init__(self):
        """constractor"""
        self.client = pymongo.MongoClient('localhost', 27017)

    def getDB(self, dbName:str):
        self.db = self.client['{}'.format(dbName)]
        return self.db

    def getCollection(self, colName) -> pymongo.collection.Collection:
        """collection of MongoDB is like a table of RDB"""
        """collection is activated when a first doc is inserted. It's not when the collection is created"""
        self.col = self.db['{}'.format(colName)]
        return self.col

    def insertOneDoc(self, post) -> ObjectId:
        """insert a single Doc(post) into db"""
        """return ObjectId of the post"""
        # posts = self.db.posts
        return self.col.insert_one(post).inserted_id

    def insertManyDocs(self, newPosts:list) -> ObjectId:
        """insert many Docs(posts) into db"""
        """return list of ObjectId which are inserted"""
        return self.col.insert_many(newPosts).inserted_ids

    def getSingleDoc(self, query:dict) -> dict:
        """query in db and return the first match of Doc as dict"""
        return self.col.find_one(query)

    def getSingleDocById(self, id:str) -> dict:
        """query in db by id return result as dict"""
        objectId = ObjectId(id)
        return self.col.find_one({'_id':objectId})

    def getAllDocs(self) -> pymongo.cursor.Cursor:
        """get all docs as Curosor instance. Need 'for' control to get each doc"""
        return self.col.find()

    def getSpecificDocs(self, query:dict) -> pymongo.cursor.Cursor:
        """get docs using query. Need 'for' control to get each doc"""
        return self.col.find(query)

        #TODO : delete function needed
