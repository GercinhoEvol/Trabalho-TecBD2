import oauth2

# Variaveis de autentificacao na ApiTwitter
consumer_Key = 'XELDltS01IxUMQDMDlTP5Tax5'
consumer_Secret = 'z6rGY8x1ZQ4g7Jhre9OrF9O3t5P0yFs8iRqaaPDgG0ioxtVev8'

token_key = '4238064022-OKb4QxPDCtalC26R3D39SZoJhBcsixrhozKJIvm'
token_Secret = 'ELqC5lBvrgyUFWRVwVU4wA09bSL6isx9DcFrTTqwbWwTp'

# Variaveis de autentificacao na ApiTwitter
consumer_Key2 = 'x8AuZEC11017lS6nnaaIgXXPQ'
consumer_Secret2 = 'HwnStdiAEX50RUNgbvM25ygiY6EU7yHfiJHzVsfjPrImweWBSS'

token_key2 = '4238064022 - QmWT1mZUjwmxQMNXzLKJWW0Ck3URR8QtRLce3IV'
token_Secret2 = 'ypOOus4ye8MreFCbOJ73QRfDqVC4bjzW05FGsQJgZPcEX'

# Variaveis de autentificacao na ApiTwitter
consumer_Key3 = 'Eo09BBIr3jpbdYpLDh21OKL1R'
consumer_Secret3 = '6ubvIzhk5KA1ssxsVBbvgwL1QpuX3ZnZaYccTvC0Us3gSw9YaR'

token_key3 = '904865034525974528-gVCTYMRONRtM6OVxXYQkjofT81MChnw-OKb4QxPDCtalC26R3D39SZoJhBcsixrhozKJIvm'
token_Secret3 = 'DIoWGZ7bpYVwFaVevoycyFGfzdAQOsYi5EI6775kgFXMc'

# Variaveis de autentificacao na ApiTwitter
consumer_Key4 = ''
consumer_Secret4 = ''

token_key4 = ''
token_Secret4 = ''


def Chave(status):
    if status == 0:
        cliente = Token()

    elif status == 1:
        cliente = Token2()

    elif status == 2:
        cliente = Token3()

        # elif status == 3:
        # cliente = Token4()

    return cliente


def Token():
    consumer = oauth2.Consumer(consumer_Key, consumer_Secret)
    token = oauth2.Token(token_key, token_Secret)

    cliente = oauth2.Client(consumer, token)

    return cliente


def Token2():
    consume = oauth2.Consumer(consumer_Key2, consumer_Secret2)
    toke = oauth2.Token(token_key2, token_Secret2)

    client = oauth2.Client(consume, toke)

    return client


def Token3():
    consume = oauth2.Consumer(consumer_Key3, consumer_Secret3)
    toke = oauth2.Token(token_key3, token_Secret3)

    client = oauth2.Client(consume, toke)

    return client


def Token4():
    consume = oauth2.Consumer(consumer_Key4, consumer_Secret4)
    toke = oauth2.Token(token_key4, token_Secret4)

    client = oauth2.Client(consume, toke)

    return client
