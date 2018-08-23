import MongoDBManager

manager = MongoDBManager.MongoDBManager();
sampleDB = manager.getDB("stocks")
col = manager.getCollection('stocks')
# print(type(col))
# print(col)
# id = manager.insertOneDoc({'company':'Rakuten','price':'800','date':'2018.08.23'})
# inserted_id = manager.getSingleDoc({'test2':'aaaa'})
# print(type(inserted_id))
# print(inserted_id)
# all = manager.getAllDocs()
# print(type(all))
# for each in all:
#     print(each)
#     print(each['company'])
res = manager.getSpecificDocs({'company':'AAPL'})
for each in res:
    print(each)
