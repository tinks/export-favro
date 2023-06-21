from setup_database import setup_db
from populate_tags import populate_tags
from populate_users import populate_users
from populate_collections import populate_collections
from populate_widgets import populate_widgets
from populate_custom_fields import populate_custom_fields
from populate_cards import populate_cards
from populate_comments import populate_comments

def export_favro():
    print ('Creating database')
    setup_db()
    print ('Populating tags')
    populate_tags()
    print ('Populating users')
    populate_users()
    print ('Populating collections')
    populate_collections()
    print ('Populating widgets and collection dependencies')
    populate_widgets()
    print ('Populating available custom fields')
    populate_custom_fields()
    print ('Populating cards and downloading attachments')
    populate_cards()
    print ('Populating comments and downloading attachments')
    populate_comments()

if __name__ == '__main__':
    export_favro()