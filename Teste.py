import pymongo
import pprint
soma = 0
conn = pymongo.MongoClient()

db = conn['Congress']
db2 = conn['Tweets']

def DupsRemover():
    pipeline = [{'$group': {'_id': '$Tweet', 'count': {'$sum': 1}, 'ids': {'$push': '$_id'}}},
                {'$match': {'count': {'$gte': 2}}}]
    request = []
    i= 0
    for nome in db2.collection_names():
        col= db2[nome]
        for document in col.aggregate(pipeline):
            it = iter(document['ids'])
            next(it)
            for id in it:
                request.append(pymongo.DeleteOne({'_id': id}))
                col.bulk_write(request)
                i= i+1
                print 'delete: %s'%(i)
    pass

#excluir todas as collections
#for c in db2.collection_names():
    #db2.drop_collection(c)

#test = 35838
#coll = db2['PATRUS ANANIAS']

print db.collection_names()
print db2.collection_names()

for list in db2.collection_names():
    col = db2[list]
    soma = soma + col.count()
    print col.count()
    for twe in col.find():
        print twe

print soma
print

#DupsRemover()

print 'The End'