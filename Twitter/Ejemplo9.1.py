"""
Ejemplo 9-1 accesando al API de Twitter para desarrollar.

Modificado para accesar a un archivo con las credenciales y evitar el hardcoding
de estas.
"""
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

#Ejemplo de uso
twitter_api=oauth_login('oaut.txt')

print twitter_api