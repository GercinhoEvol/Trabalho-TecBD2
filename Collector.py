import pymongo
import json
import time
import re

from TokenRotation import Chave





# Cria conexao com Mongo
conn = pymongo.MongoClient()

# Acessa base de dados pre carregada com politicos
db = conn['Congress']

#Cria e mantem acesso a base de dados com tweets dos politicos
db2 = conn['Tweets']

# URL de busca da ApiTwitter
BASE_URL = "https://api.twitter.com/1.1/search/tweets.json"

#contador tweets global
tweetscount = 0


tempo = [0,0,0,0]

def Temporizador(status, tempo):
    run = False
    i = 0

    while run != True:
        if time.time() > tempo[0]:
            status = 0
            run = True
        elif time.time() > tempo[1]:
            status = 1
            run = True
        elif time.time() > tempo[2]:
            status = 2
            run = True
            # elif time.time()> tempo[3]:
            # status = 3
            # run = True
        else:
            i = i + 1
            print('Sleep: %s'%(i))
            time.sleep(60)
            run = False

        result = Search('#brasil', 10, 0, status)
        if result.get('code', None) == 88:
            run = False
        else:
            run = True
    return status

# Retira do tweet caracteres desnecessarios
def Processador(text):
    result = re.sub(r"http\S+", "", text)
    result = re.sub('[!@#$.]','', result)
    return result

#metodo de Busca na ApiTwitter
def Search(keyword, n, max_id, status):

    cliente = Chave(status)

    url = BASE_URL + ("?q=%s&count=%d" % (keyword, n))

    if max_id is not None:
         url = url + "&max_id=%d" % (max_id)

    requisicao = cliente.request(url)

    Dcode = requisicao[1].decode()
    objeto = json.loads(Dcode)
    #print objeto
    return objeto

# Metodo de Insert do twitter no Mongodb
def TweetInsert(result, coll):
    global tweetscount
    i = 0
    for tweet in result.get('statuses', None):
        twet = tweet.get('user', None)

        Ninter = twet.get('scream_name', None)
        text = tweet.get('text', None)
        id_str = tweet.get('id_str', None)

        m = result.get('search_metadata', None)
        im = m.get('max_id', None)


        text = Processador(text)
       # print text

        post = [{
            'Post': {"Internauta": Ninter, "Tweet": text, "Id_str": id_str}, }]

        coll.insert(post)
        coll.update_one({'Max_Id': 1}, {'$set': {'Max_Id': im}}, upsert= True)
        i = i+1
        tweetscount = i

       # print post
    pass

def Reads(quer):
    # Acessa cada Collection
    coll = db[quer]

    #reads = coll.find({}).batch_size(10)
    reads = coll.find(no_cursor_timeout=True)
    return reads


# Inicia coletor Na ApiTwitter
def MainBoot(quer, status):
    i = x = run = 0
    while run <= 10:
        for read in Reads(quer):

            cargo = read['Congressista']['Cargo']
            nome = read['Congressista']['Nome']

            quest = cargo + ' ' + nome
            print ("%s %s: %s" % (cargo, i+1, nome))

            coll = db2[nome]
            mid = coll.find_one('Max_Id')

            result = Search(quest, 100, mid, status)

            i = i + 1
            try:
                TweetInsert(result, coll)
                print ("%s Tweets salvo" % (tweetscount))
            except:
                #if result.get('code', None) == 88:
                    x = x+1
                    tempo.insert(status, time.time() + (60*15))

                    print("Erro: %s, %s" % (x, time.strftime("%H:%M,%S", time.gmtime())))
                    status = Temporizador(status, tempo)
                    print("Continue : %s" % (time.strftime("%H:%M,%S", time.gmtime())))

                    #result = Search(quest, 100, mid, status)

                    #TweetInsert(result, coll)

            run = run + 1