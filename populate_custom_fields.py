from favro_request import make_request
from db_actions import populate_db

def populate_custom_fields():
    url = 'https://favro.com/api/v1/customfields'
    custom_fields = make_request(url)

    ## create the list of values to populate in the db
    custom_field_values = []
    custom_field_item_values = []
    for custom_field in custom_fields:
        custom_field_value = (custom_field['customFieldId'],custom_field['name'],custom_field['type'],custom_field['enabled'])
        custom_field_values.append(custom_field_value)
        if "customFieldItems" in custom_field:
            for item in custom_field['customFieldItems']:
                custom_field_item_value = (item['customFieldItemId'],custom_field['customFieldId'],item['name'])
                custom_field_item_values.append(custom_field_item_value)

    # populate the custom fields in the database
    query_custom_fields = "INSERT INTO custom_field (id, name, type, enabled) VALUES (?, ?, ?, ?)"
    populate_db(query_custom_fields, custom_field_values)

    query_custom_field_items = "INSERT INTO custom_field_item (id, custom_field_id, name) VALUES (?, ?, ?)"
    populate_db(query_custom_field_items, custom_field_item_values)