from favro_request import make_request
from db_actions import populate_db

def populate_collections():
    url = 'https://favro.com/api/v1/collections'
    collections = make_request(url)

    # create the list of values to populate in the db
    values = []
    for collection in collections:
        value = (collection['collectionId'],collection['name'])
        values.append(value)


    # populate the database
    query = "INSERT INTO collection (id, name) VALUES (?, ?)"
    populate_db(query, values)
