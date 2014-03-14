"""
Ejemplo 9.3 - Encontrar los TT

"""

import json
import twitter

def oauth_login(archivo):
    

    #Leer el archivo donde estan las credenciales
    lines = [line.strip() for line in open(archivo)]
    
    #Obtener las credenciales para la API de twitter
    _consumer_key=lines[0]
    _consumer_secret=lines[1]
    _oauth_token=lines[2]
    _oauth_token_secret=lines[3]

    auth=twitter.oauth.OAuth(_oauth_token,_oauth_token_secret,_consumer_key,_consumer_secret)

    twitter_api=twitter.Twitter(auth=auth)
    return twitter_api

def twitter_TT(twitter_api, woe_id):
    """
    woe_id lo puedes obtener utilizando google.
    A la variable ID le agregamos un _ para la parametrizacion de cadenas.
    Si no se le pone el _, el paquete twitter le agrega el valor de ID a la URL
    como un argumento de caso especial.
    """
    return twitter_api.trends.place(_id=woe_id)

twitter_api=oauth_login('oaut.txt')


_mexico_woe_id=23424900
mexico_tt=twitter_TT(twitter_api, _mexico_woe_id)
print json.dumps(mexico_tt, indent=1)
print

_mundo_woe_id=1
mundo_tt=twitter_TT(twitter_api, _mundo_woe_id)
print json.dumps(mundo_tt, indent=1)
print

_us_woe_id=23424977
us_tt=twitter_TT(twitter_api, _us_woe_id)
print json.dumps(us_tt, indent=1)