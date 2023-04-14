from favro_request import make_request
from db_actions import populate_db

url = 'https://favro.com/api/v1/users'
users = make_request(url)

## create the list of values to populate in the db
values = []
for user in users:
    value = (user['userId'],user['name'],user['email'])
    values.append(value)

# populate the database
query = "INSERT INTO user (id, name, email) VALUES (?, ?, ?)"
populate_db(query, values)