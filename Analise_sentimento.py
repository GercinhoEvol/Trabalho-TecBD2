import pymongo
import nltk
import re
import pip as csv
import pandas as pd
from decimal import *

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics
from sklearn.model_selection import cross_val_predict

# Cria conexao com Mongo
conn = pymongo.MongoClient()

# Acessa base de dados pre carregada com politicos
db = conn['Congress']

#Acesso a base de dados com tweets dos politicos
db2 = conn['Tweets']

#contador tweets global
tweetscount = 0

    #ler e contar arqivo de 8900 tweets para treinamento
dataset = pd.read_csv('Tweets_Mg.csv',encoding='utf-8')
dataset.count()
    #separar tweets das classes
tweets = dataset['Text'].values
classes = dataset['Classificacao'].values
    #treinamento de modelo do tipo Naive Bayes Multinomial
vectorizer = CountVectorizer(ngram_range=(1,2))
freq_tweets = vectorizer.fit_transform(tweets)
modelo = MultinomialNB()
modelo.fit(freq_tweets,classes)

#setar precisao de decimal
getcontext()
Context(prec=28, rounding=ROUND_HALF_EVEN, Emin=-999999999, Emax=999999999,
        capitals=1, flags=[], traps=[Overflow, DivisionByZero,
        InvalidOperation])
getcontext().prec = 5

def SentimentoInsert(sentimentTweet, db): #Acessa e inserta Collection
    coll = db
    coll.insert({"sentimento":sentimentoTweet})
    pass


def Reads(quer):
    # Acessa cada Collection
    coll = db[quer]

    reads = coll.find().batch_size(10).max_time_ms(60*1000*60)
    return reads



# Inicia Analise de Sentimento

quer = ['Senador', 'Dep_Federal', 'Dep_Estadual', 'Vereador']
for query in quer:
    i = 0
    if query == 'Senador':

        coll1 = db[query].find()
        colll = db[query]

        for read in coll1:
            x = 0
            nome = read['Congressista']['Nome']
            idPolitco = [read['_id']]
            coll = db2[nome]
            lista = coll.find()
            posCount = 0
            neuCount = 0
            negCount = 0
            razao = 0
            for list in lista:
                #print(list)

                testes = [list['Post']['Tweet']]
                idPost = [list['_id']]
                freq_testes = vectorizer.transform(testes)
                sentimentoTweet = modelo.predict(freq_testes)
                coll.update_one(
                    {'_id': idPost[0]},
                    { "$set": {'Sentimento': sentimentoTweet[0]}}, upsert= True)
                x = x + 1

                if sentimentoTweet[0] == "Positivo":
                    posCount = posCount + 1
                if sentimentoTweet[0] == "Neutro":
                    neuCount = neuCount + 1
                if sentimentoTweet[0] == "Negativo":
                    negCount = negCount + 1
            if x != 0:
                if posCount > negCount:
                    razao = Decimal(posCount) / Decimal(x)
                else:
                    razao = Decimal(negCount) / Decimal(x)
                    razao = -razao
            coll.update_one(
                {'_id': idPolitco[0]},
                {"$set": {'RateSentimento': razao}}, upsert=True)

            i = i + x
            print ("%s Tweets analisados do %s %s com e razao de sentimento = %s" % (x, query, nome, razao))
            print list
        else:
            print "ainda vou implementar"

    print "Analisado %s Tweets de %s"% (i, query)



resultados = cross_val_predict(modelo, freq_tweets, classes, cv=10)
print ('Acuracia:')
print metrics.accuracy_score(classes,resultados)

sentimento=['Positivo','Negativo','Neutro']
print (metrics.classification_report(classes,resultados,sentimento))

print (pd.crosstab(classes, resultados, rownames=['Real'], colnames=['Predito'], margins=True))