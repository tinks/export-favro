import requests
import json
from config import API_KEY, ORGANIZATION_ID
from sys import exit
import datetime
import time

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
    elif (response.status_code == 429): # handle reaching the request limit per hour
        reset_time = datetime.datetime.fromisoformat(response.headers['X-RateLimit-Reset'])
        now = datetime.datetime.now(datetime.timezone.utc)
        diff = reset_time - now
        print ('Timestamp reset: ', reset_time)
        print ('Timestamp now: ', now)
        print ('Waiting time: ', diff)
        time.sleep(diff.total_seconds() + 10)
        make_request(url, query_params)
    
    # requests are limited to 100 entities, if there are more, then pages is greater than 1
    # to request the next page, you also need to the requestId from the first response
    if pages > 1:
        request_all_pages(url, my_headers, query, entities , pages)

    return entities

def request_all_pages(url, my_headers, query_params, entities, pages, page = 1):

    query = query_params

    while page < pages:
        query['page'] = page
        response = requests.get(url, params=query, headers=my_headers)
        if (response.status_code == 200):
            raw = json.loads(response.text)
            entities.extend(raw['entities'])
        elif (response.status_code == 400 or response.status_code == 500 ):
            print(response.status_code)
            print(response.request)
            print(response.headers)
            exit()
        elif (response.status_code == 429): # handle reaching the request limit per hour
            reset_time = datetime.datetime.fromisoformat(response.headers['X-RateLimit-Reset'])
            now = datetime.datetime.now(datetime.timezone.utc)
            diff = reset_time - now
            print ('Timestamp reset: ', reset_time)
            print ('Timestamp now: ', now)
            print ('Waiting time: ', diff)
            time.sleep(diff.total_seconds() + 10)
            request_all_pages(url, my_headers, query_params, entities, pages, page)
        page += 1
    
    return entities
