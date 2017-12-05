import pymongo
from pymongo import MongoClient
import csv
import unicodedata

#Script inicia banco de dados no mongo
#faz o Insert de todos os politicos lendo de 4 arquivos csv

try:
    conn = MongoClient('localhost', 27017)
    print "Connected successfully!!!"
except pymongo.errors.ConnectionFailure, e:
   print "Could not connect to MongoDB: %s" % e
conn



db = conn['Congress']

quer = ['Senador', 'Dep_Federal', 'Dep_Estadual', 'Vereador']
for query in quer:
    doc = query + '.csv'
    cr = csv.reader(open(doc, "rU"),delimiter=';')
    coll = db[query]
    i = 0
    for read in cr:
        if query == 'Senador':
            obj = [{"Congressista": {"Nome": read[4].decode('latin-1').encode('utf-8'), "Nome Civil": read[3].decode('latin-1').encode('utf-8'), "Partido": read[1], "Estado": read[0],
                                     "id": '', "Cargo": query}}]
            coll.insert(obj)
        else:
            obj = [{"Congressista": { "Nome": read[4].decode('latin-1').encode('utf-8'), "Nome Civil":  read[3].decode('latin-1').encode('utf-8'), "Partido":  read[1], "Estado": read[0], "id": '', "Cargo": read[5]}}]
            coll.insert(obj)

        i = i + 1
    print "%s %s"% (query, i)