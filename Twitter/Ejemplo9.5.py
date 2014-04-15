"""
9.5 Construyendo llamadas a funciones mas convenientes

investigar mas sobre funcion partial

"""

from functools import partial
import json

#pp = pretty print

pp = partial(json.dumps, indent=1)

twitter_world_trends=partial(twitter_trends, twitter_api, world_woe_id)
print pp(twitter_world_trends())

authenticated_twitter_search=partial(twitter_search, twitter_api)
results = authenticated_twitter_search("iphone")
print pp(results)

authenticated_iphone_twitter_search = partial(authenticated_twitter_search, "iphone")
results = authenticated_iphone_twitter_search()
print pp(results)