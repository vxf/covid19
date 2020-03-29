import requests
from cache import request_cache

"""
Fetch data from https://covid19.min-saude.pt/ponto-de-situacao-atual-em-portugal/
"""

url = 'https://services.arcgis.com/CCZiGSEQbAxxFVh3/arcgis/rest/services/COVID19Portugal_view/FeatureServer/0/query'

MAX_AGE = 3600 # 1 hour, let's not overwelm the services
CACHE_DIR = '.cache'

@request_cache(max_age=MAX_AGE, cache_dir=CACHE_DIR)
def request_data_json(where = 'objectid IS NOT NULL'):
    params = {
        'f' : 'json',
        'where' : where,
        'returnGeometry' : 'false',
        'spatialRel' : 'esriSpatialRelIntersects',
        'outFields' : '*',
        'orderByFields' : 'datarelatorio asc',
        'resultOffset' : '0',
        'resultRecordCount' : '1000',
        'cacheHint' : 'true',
    }

    resp = requests.get(url=url, params=params)
    return resp.json()

def get_attributes():
    data = request_data_json()

    for f in data['fields']:
        yield (f['alias'], f['name'])

def get_alias(attributes, name):
    for a, n in attributes:
        if n == name:
            return a

def get_attribute_header(attribute):
    attributes = get_attributes()
    datarelatorio_alias = get_alias(attributes, 'datarelatorio')
    attribute_alias = get_alias(attributes, attribute)

    return (datarelatorio_alias, attribute_alias)

def get_attribute_data(attribute):
    data = request_data_json('{} IS NOT NULL'.format(attribute))

    for f in data['features']:
        timestamp = f['attributes']['datarelatorio']
        value = f['attributes'][attribute]

        yield (timestamp, value)
