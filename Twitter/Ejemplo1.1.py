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

_mundo_tt=twitter_api.trends.place(_id=_mundo_woe_id)
_usa_tt=twitter_api.trends.place(_id=_usa_woe_id)

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

"""
Ejemplo 1.3 Mostrar las respuestas de la API como JSON con formato

"""

import json
print json.dumps(_mundo_tt, indent=1)
print
print json.dumps(_usa_tt, indent=1)
print

"""
Ejemplo 1.4 Calculando la interseccion de dos sets de TT

"""

_set_mundo=set([trend['name'] for trend in _mundo_tt[0]['trends']])
_set_usa=set([trend['name'] for trend in _usa_tt[0]['trends']])

_tt_comun=_set_mundo.intersection(_set_usa)

print _tt_comun
print
