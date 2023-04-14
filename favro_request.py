import requests
import json
from config import API_KEY, ORGANIZATION_ID
from sys import exit

def make_request(url, query_params = {}):
    my_headers = {'Authorization': API_KEY, 'organizationId': ORGANIZATION_ID}
    pages = 1
    query = {'requestId': 'xxx', 'page': 0}
    query.update(query_params)
    entities = []
    response = requests.get(url, params=query, headers=my_headers)

    if (response.status_code == 200):
        raw = json.loads(response.text)
        query['requestId'] = raw['requestId']
        pages = raw['pages']
        entities = raw['entities']
        my_headers['X-Favro-Backend-Identifier'] = response.headers['X-Favro-Backend-Identifier']
    elif (response.status_code == 400 or response.status_code == 500 ):
        print(response.status_code)
        print(response.request)
        print(response.headers)
        exit()
    elif (response.status_code != 403):
        print(response.status_code)
        print(response.headers)
        exit()
    
    # requests are limited to 100 entities, if there are more, then pages is greater than 1
    # to request the next page, you also need to the requestId from the first response
    page = 1
    while page < pages:
        query['page'] = page
        response = requests.get(url, params=query, headers=my_headers)
        if (response.status_code == 200):
            raw = json.loads(response.text)
            entities.extend(raw['entities'])
        page += 1
    
    return entities
