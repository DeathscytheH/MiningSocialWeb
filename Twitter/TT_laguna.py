"""
Encontrar TT en comun en la laguna

"""
#1. Loguearme en la API
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


#2. Obtener TT de la laguna y Mexico (Pais)
try:
    """
    Twitter aun no soporta localizacion de TT via woeid para algunos paises. 
    Encontrar otra solucion
    """
    _mexico_woe_id=23424900
    _gomez_woe_id=12599957
    _torreon_woe_id=12599920
    _lerdo_woe_id=12599962
    _lalaguna_woe_id=90317919
    _durango_woe_id=2346273
    _coahuila_woe_id=2346270

    _mexico_tt=twitter_api.trends.place(_id=_mexico_woe_id)
    #_coauila_tt=twitter_api.trends.place(_id=_coahuila_woe_id)
    #_durango_tt=twitter_api.trends.place(_id=_durango_woe_id)
    #_torreon_tt=twitter_api.trends.place(_id=_torreon_woe_id)
    #_gomez_tt=twitter_api.trends.place(_id=_gomez_woe_id)
    #_lerdo_tt=twitter_api.trends.place(_id=_lerdo_woe_id)
    #_lalaguna_tt=twitter_api.trends.place(_id=_lalaguna_woe_id)
except twitter.TwitterHTTPError, e:
    print "Error 404, no se encontro la locacion"
    print
    print e
      

#3. Mostrar TT en JSON

import json
print json.dumps(_mexico_tt, indent=1)
print
"""
print json.dumps(_torreon_tt, indent=1)
print
print json.dumps(_gomez_tt, indent=1)
print
print json.dumps(_lerdo_tt, indent=1)
print
print json.dumps(_lalaguna_tt, indent=1)
print

#4.Crear los set y encontrar similitudes

_set_mexico=set([trend['name'] for trend in _mexico_tt[0]['trends']])
_set_torreon=set([trend['name'] for trend in _torreon_tt[0]['trends']])
_set_gomez=set([trend['name'] for trend in _gomez_tt[0]['trends']])
_set_lerdo=set([trend['name'] for trend in _lerdo_tt[0]['trends']])
_set_lalaguna=set([trend['name'] for trend in _lalaguna_tt[0]['trends']])

_tt_comun_mexico_laguna=_set_mexico.intersection(_set_lalaguna)
_tt_comun_laguna=_set_lalaguna.intersection(_set_lerdo,_set_torreon,_set_gomez)

print _tt_comun_mexico_laguna
print
print _tt_comun_laguna
"""