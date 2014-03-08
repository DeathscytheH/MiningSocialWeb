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

_mexico_woe_id=23424900
_torreon_woe_id=149893
_gomez_woe_id=124050
_lerdo_woe_id=116557
_lalaguna_woe_id=90317919

_mexico_tt=twitter_api.trends.place(_id=_mexico_woe_id)
_torreon_tt=twitter_api.trends.place(_id=_torreon_woe_id)
_gomez_tt=twitter_api.trends.place(_id=_gomez_woe_id)
_lerdo_tt=twitter_api.trends.place(_id=_lerdo_woe_id)
_lalaguna_tt=twitter_api.trends.place(_id=_lalaguna_woe_id)

