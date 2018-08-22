import pymongo

class MongoDBManager:
    def __init__(self):
        """constractor"""
        self.client = MongoClient('localhost', 27017)

    def getDB(self, dbName:str):
        self.db = self.client['{}'.format(dbName)]
        return self.db

    def getCollection(self, colName):
        """collection of MongoDB is like a table of RDB"""
        self.col = self.db['{}'.format(colName)]
        return self.col

    def insertOneDoc(self, post:json):
        """insert a single Doc(post) into db"""
        """return ObjectId of the post"""
        posts = self.db.posts
        return posts.insert_one(post).inserted_id

    def insertManyDocs(self, newPosts:list):
        """insert many Docs(posts) into db"""
        """return list of ObjectId which are inserted"""
        posts = self.db.posts
        return posts.insert_many(newPosts).inserted_ids

    def getSingleDoc(self, query:dict = {'_id':ObjectId(1)}):
        """query in db and return the first match of Doc"""
        posts = self.db.posts
        return posts.find_one(query)

    def getSingleDocById(self, id:str):
        """query in db by id"""
        posts = self.db.posts
        return posts.find_one({'_id':ObjectId(id)})

    def getAllDocs(self):
        """get all docs"""
        return self.db.posts.find()

    def getSpecificDocs(self, query:dict):
        """get docs using query"""
        return self.db.posts.find(query)
