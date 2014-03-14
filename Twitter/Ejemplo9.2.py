"""
Ejemplo 9.2 - Implementando OAuth para una aplicacion de produccion

revisar que onda con el 0.0.0.0:5000
"""

import json
from flask import Flask, request
import multiprocessing
from threading import Timer
from IPython import IFrame, display, Javascript as JS

import twitter
from twitter.oauth_dance import parse_oauth_tokens
from twitter.oauth import read_token_file, write_token_file

#El archivo al que va a salir todo
OAUTH_FILE="oauth_file.txt"

#Definir algunas variables que se usaran en algunas funciones siguientes

CONSUMER_KEY=''
CONSUMET_SECRET=''
oauth_callback='http://127.0.0.1:5000/oauth_helper'

#Poner un manejador para cuando la llamada regrese despues de que el usuario
#autorize el app

webserver=Flask("TwitterOAuth")
@webserver.route("/oauth_helper")

def oauth_helper():
    
    oauth_verifier=request.args.get('oauth_verifier')
    
    #Recojer credenciales de respaldo
    oauth_token, oauth_token_secret=read_token_file(OAUTH_FILE)
    
    _twitter=twitter.Twitter(auth=twitter.OAuth(oauth_token, oauth_token_secret, CONSUMER_KEY, CONSUMET_SECRET), format='', api_version=None)
    
    oauth_token, oauth_token_secret=parse_oauth_tokens(_twitter.oauth.access_token(oauth_verifier=oauth_verifier))
    
    #Este web server solo necesita servir una peticion, asi que se apaga
    shutdown_after_request=request.environ.get('werkzeug.server.shutdown')
    shutdown_after_request()
    
    #Se escriben las credenciales 
    write_token_file(OAUTH_FILE, oauth_token, oauth_token_secret)
    return "%s %s se escribio en %s" % (oauth_token, oauth_token_secret, OAUTH_FILE)

# Para manejar la implementacion OAuth 1.0a de Twitter, se implementara una 
# modificacion del "oauth dance" y seguira muy de cerca el patron definido en 
# twitter.oauth_dance

def py_oauth_dance():
    
    _twitter=twitter.Twitter(auth=twitter.OAuth('','',CONSUMER_KEY, CONSUMET_SECRET), format='', api_version=None)
    
    oauth_token, oauth_token_secret = parse_oauth_tokens(_twitter.oauth.request_token(oauth_callback=oauth_callback))
    
    # Se nececitan escribir estos valores en un archivo para de ahi recojer la 
    # llamada de Twitter que es manejada del web server en /oauth_helper
    
    write_token_file(OAUTH_FILE,oauth_token, oauth_token_secret)
    
    oauth_url=('http://api.twitter.com/oauth/authorize?oauth_token='+oauth_token)
    
    #Utilizamos el browser para abrir una nueva ventana y asi accesar al web 
    #server y obtener la autorizacion del usuario
    display(JS("windows.open('%s')" % oauth_url))

"""
Despues de la llamada de bloqueo a webserver.run(), inicia el OAuth Dance que 
hara que twitter haga una redireccion de una peticion hacia el. Ya que se haya
servido esa peticion, el server se apagara y el programa continuara. Sin embargo,
el OAUTH_FILE contendra las credenciales necesarias.
"""

Timer(1, lambda: py_oauth_dance()).start()

webserver.run(host='0.0.0.0')

#Los valores que son leidos del archivo se escriben al final de /oauth_helper

oauth_token, oauth_token_secret=read_token_file(OAUTH_FILE)

#Estas cuatro credenciales son las que se requieren para autorizar la app

auth=twitter.oauth.OAuth(oauth_token,oauth_token_secret,CONSUMER_KEY, CONSUMET_SECRET)

twitter_api=twitter.Twitter(auth=auth)

print twitter_api