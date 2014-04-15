"""
9.6 salvando y recuperando datos JSON de archivos txt

"""
import twitter

def oauth_login(archivo):
    

    #Leer el archivo donde estan las credenciales
    lines = [line.strip() for line in open(archivo)]
    
    #Obtener las credenciales para la API de twitter
    
    _consumer_key, _consumer_secret, _oauth_token, _oauth_token_secret=lines

    auth=twitter.oauth.OAuth(_oauth_token,_oauth_token_secret,_consumer_key,_consumer_secret)

    twitter_api=twitter.Twitter(auth=auth)
    return twitter_api

def twitter_search(twitter_api, q, max_results=200, **kw):

    # Revisar https://dev.twitter.com/docs/api/1.1/get/search/tweets y
    # https://dev.twitter.com/docs/using-search por detalles para busquedas avanzadas   
    search_results = twitter_api.search.tweets(q=q, count=100, **kw)
    
    statuses = search_results['statuses']
    
    # Iterate through batches of results by following the cursor until we
    # reach the desired number of results, keeping in mind that OAuth users
    # can "only" make 180 search queries per 15-minute interval. See
    # https://dev.twitter.com/docs/rate-limiting/1.1/limits
    # for details. A reasonable number of results is ~1000, although
    # that number of results may not exist for all queries.
    
    # Enforce a reasonable limit
    max_results = min(1000, max_results)
    
    for _ in range(10): # 10*100 = 1000
        try:
            next_results = search_results['search_metadata']['next_results']
        except KeyError, e: # No more results when next_results doesn't exist
            break
            
        # Create a dictionary from next_results, which has the following form:
        # ?max_id=313519052523986943&q=NCAA&include_entities=1
        kwargs = dict([ kv.split('=') 
                        for kv in next_results[1:].split("&") ])
        
        search_results = twitter_api.search.tweets(**kwargs)
        statuses += search_results['statuses']
        
        if len(statuses) > max_results: 
            break
            
    return statuses

import io, json

def save_json(filename, data):
    with io.open('{0}.json'.format(filename), 'w', encoding='utf-8') as f:
        f.write(unicode(json.dumps(data, ensure_ascii=False)))
        
def load_json(filename):
    with io.open('{0}.json'.format(filename), encoding='utf-8') as f:
        return f.read()

#Ejemplo de uso

q='mujerlunabella'

twitter_api=oauth_login('oaut.txt')
results = twitter_search(twitter_api, q, max_results=10)

save_json(q, results)
results = load_json(q)

print json.dumps(results, indent=1)