from favro_request import make_request
from db_actions import populate_db

url = 'https://favro.com/api/v1/tags'
tags = make_request(url)

## create the list of values to populate in the db
values = []
for tag in tags:
    value = (tag['tagId'],tag['name'])
    values.append(value)

# populate the database
query = "INSERT INTO tag (id, name) VALUES (?, ?)"
populate_db(query, values)