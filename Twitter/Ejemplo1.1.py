# -*- coding: utf-8 -*-
"""
Mining the social web 2.0

1.
Obtener de un usuario todos los tweets donde aparescan links y resolverlos en 
busca de fotografias.
En base a las fotografias, analisar los metadatos de estas y buscar 
localizaciones.
Crear un mapa en base a esas localizaciones.

2. De un usuario, buscar todos los tweets donde aparescan posicion gps.
crear un mapa
"""

"""
Ejemplo 1.1

Autorizando una app para accesar a los datos de cuenta de twitter

"""

#Leer el archivo donde estan las credenciales
lines = [line.strip() for line in open('oaut.txt')]

import twitter

#Obtener previamente las credenciales para la API de twitter

_consumer_key=lines[0]
_consumer_secret=lines[1]
_oauth_token=lines[2]
_oauth_token_secret=lines[3]

auth=twitter.oauth.OAuth(_oauth_token,_oauth_token_secret,_consumer_key,_consumer_secret)

twitter_api=twitter.Twitter(auth=auth)

#print twitter_api

"""
Ejemplo 1.2

Recuperando TT

WOE ID identificador de donde en el mundo
lo tiene yahoo, un api, registrarse
"""

_mundo_woe_id=1
_usa_woe_id=23424977
_mexico_woe_id=23424900

_mundo_tt=twitter_api.trends.place(_id=_mundo_woe_id)
_usa_tt=twitter_api.trends.place(_id=_usa_woe_id)
_mexico_tt=twitter_api.trends.place(_id=_mexico_woe_id)

#Se regresan diccionarios

"""
Patron para usar este modulo de twitter

Instanciar la clase Twitter con una cadena de objetos que corresponde a la url
base y despues invocar los meotodos en el objeto que corresponde a los contextos
de la url.
Ejemplo
twitter_api.trends.place(_id=_mundo_woe_id)
hace una llamada GET a https://api.twitter.com/1.1/trends/place.json?id=1

Es de notar que el mapeo de la cadena de objetos la cual esta construida con el
paquete de twitter para hacer la peticion y como los parametros son pasados como
argumentos.
Si queremos hacer peticiones al API con parametros arbitrarios hay que contruirlos
de esta manera.
"""

print _mundo_tt
print
print _usa_tt
print
print _mexico_tt
print

"""
Ejemplo 1.3 Mostrar las respuestas de la API como JSON con formato

"""

import json
print json.dumps(_mundo_tt, indent=1)
print
print json.dumps(_usa_tt, indent=1)
print
print json.dumps(_mexico_tt, indent=1)
print

"""
Ejemplo 1.4 Calculando la interseccion de dos sets de TT

"""

_set_mundo=set([trend['name'] for trend in _mundo_tt[0]['trends']])
_set_usa=set([trend['name'] for trend in _usa_tt[0]['trends']])
_set_mexico=set([trend['name'] for trend in _mexico_tt[0]['trends']])

print "Trending Topics"
print
print 'Mexico',_set_mexico
print
print 'US',_set_usa
print
print 'Mundo',_set_mundo
print

_tt_comun_mundo_usa=_set_mundo.intersection(_set_usa)
_tt_comun_mundo_mexico=_set_mundo.intersection(_set_mexico)
_tt_comun_mexico_usa=_set_mexico.intersection(_set_usa)
_tt_comun_mundo_usa_mexico=_set_mundo.intersection(_set_usa,_set_mexico)

print "Intersecciones"
print
print "Mundo y US",_tt_comun_mundo_usa
print
print "Mundo y Mexico",_tt_comun_mundo_mexico
print
print "Mundo, Mexico y Us",_tt_comun_mundo_usa_mexico
print
print "Mexico y US",_tt_comun_mexico_usa
print

"""
Ejemplo 1.5 Guardando resultados de busquedas

La variable q pueder utilizada para buscar no solo hashtags sino cualquier
paralabra o lo que quieras buscar.
"""

#Hastag que voy a buscar.

q="mujerlunabella"

count = 100

search_results=twitter_api.search.tweets(q=q, count = count)

statuses= search_results['statuses']

#Iteramos por otros 5 grupos de resultados siguiendo el cursor.
for _ in range(5):
    print "Tamaño de los status", len(statuses)
    try:
        next_results=search_results['search_metadata']['next_results']
        #El campo search_metada tambien contiene  un valor refresh_url que puede
        #utilizarse para mantener y actualizar los resultados con info nueva
    except KeyError, e:
        break
        
    #Se crea un diccionario de los siguientes resultados
    
    kwargs=dict([kv.split('=') for kv in next_results[1:].split('&')])
    
    #Se utiliza *args y **kwargs como parametros en una funcion, estos son idiomas
    #de python que sirven para expresar argumentos arbitrarios y argumentos de 
    #palabras claves arbitrarios, respectivamente
    
    search_results=twitter_api.search.tweets(**kwargs)
    statuses+=search_results['statuses']
    
print json.dumps(statuses[0], indent=1)

"""
Ejemplo 1.6 Extrallendo texto, username y #

List comprehensions se utiliza mucho
"""


status_texts=[status['text'] for status in statuses]

screen_names=[user_mention['screen_name'] for status in statuses for user_mention in status['entities']['user_mentions']]

hashtags=[hashtag['text'] for status in statuses for hashtag in status['entities']['hashtags']]

#Calcula una coleccion de todas las palabras de todos los tweets
words = [w for t in status_texts for w in t.split()]

#Explorar los primeros 5 items
print json.dumps(status_texts[0:5],indent=1)
print json.dumps(screen_names[0:5],indent=1)
print json.dumps(hashtags[0:5], indent=1)
print json.dumps(words[0:5],indent=1)

"""
Ejemplo 1-7 Creando una distribucion de frecuencia basica en base a las 
palabras en los tweets
"""

from collections import Counter

for item in [words, screen_names, hashtags]:
    c = Counter(item)
    print c.most_common()[:10] #Top 10
    print
    
"""
Ejemplo 1-8 Utilizando prettytable para mostrar las tuplas en una forma bonita

"""

from prettytable import PrettyTable

for label, data in (('Word', words),('Screen Name', screen_names),('Hashtag', hashtags)):
    pt=PrettyTable(field_names=[label, 'Count'])
    c=Counter(data)
    [pt.add_row(kv) for kv in c.most_common()[:10]] #Top 10
    pt.align[label], pt.align['Count']='l','r' #Alineacion de las columnas
    print pt

"""
Ejemplo 1-9 Calculando la diversidad lexica para los tweets

"""

#Una funcion para calcular la diversidad lexica

def lexical_diversity(tokens):
    return 1.0*len(set(tokens))/len(tokens)

def average_words(statuses):
    total_words=sum([len(s.split()) for s in statuses])
    return 1.0*total_words/len(statuses)

print
print "lexical diversity words", lexical_diversity(words)
print "lexical diversity screen names", lexical_diversity(screen_names)
print "lexical diversity hash", lexical_diversity(hashtags)
print "average words status texts", average_words(status_texts)
print

"""
Ejemplo 1-10 Encontrar los retweets mas populares
"""

#Guarda en una tupla estos tres valores por cada status mientras cumpla la 
#condicion
retweets=[(status['retweet_count'], status['retweeted_status']['user']['screen_name'],status['text']) for status in statuses if status.has_key('retweeted_status')]

#Mostramos solo los primeros 5 resultados y mostramos los primeros items en 
#cada tupla

pt= PrettyTable(field_names=['Count', 'Screen Name', 'Text'])

[pt.add_row(row) for row in sorted(retweets, reverse=True)[:5]]
pt.max_width['Text']=50
pt.align='l'
print pt