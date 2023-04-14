from favro_request import make_request
from db_actions import populate_db

url = 'https://favro.com/api/v1/customfields'
custom_fields = make_request(url)

## create the list of values to populate in the db
values = []
for custom_field in custom_fields:
    value = (custom_field['customFieldId'],custom_field['name'],custom_field['type'])
    values.append(value)

# populate the database
query = "INSERT INTO custom_field (id, name, type) VALUES (?, ?, ?)"
populate_db(query, values)