"""
Ejemplo 9.2 - Implementando OAuth para una aplicacion de produccion
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
OAUTH_FILE="oauth.txt"

#Definir algunas variables que se usaran en algunas funciones siguientes

CONSUMER_KEY=''
CONSUMET_SECRET=''
oauth_callback='http://127.0.0.1:5000/oauth_helper'

#Poner un manejador para cuando la llamada regrese despues de que el usuario
#autorize el app

webserver=Flask("TwitterOAuth")
@webserver.route("/oauth_helper")

