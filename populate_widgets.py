from favro_request import make_request
from db_actions import populate_db

def populate_widgets():
    url = 'https://favro.com/api/v1/widgets'
    widgets = make_request(url)

    ## create the list of values to populate in the db
    widget_values = []
    widget_to_collection_values = []
    for widget in widgets:
        value = (widget['widgetCommonId'],widget['name'])
        widget_values.append(value)
        collections = widget['collectionIds']
        for collection in collections:
            w_c_value = (widget['widgetCommonId'],collection)
            widget_to_collection_values.append(w_c_value)

    # populate the widgets in database
    query = "INSERT INTO widget (id, name) VALUES (?, ?)"
    populate_db(query, widget_values)

    # populate the widget to collection relationship in database
    query = "INSERT INTO widget_to_collection (widget_id, collection_id) VALUES (?, ?)"
    populate_db(query, widget_to_collection_values)