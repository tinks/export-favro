from setup_database import setup_db
from populate_tags import populate_tags
from populate_users import populate_users
from populate_collections import populate_collections
from populate_widgets import populate_widgets
from populate_custom_fields import populate_custom_fields
from populate_cards import populate_cards
from populate_comments import populate_comments

def export_favro():
    setup_db()
    populate_tags()
    populate_users()
    populate_collections()
    populate_widgets()
    populate_custom_fields()
    populate_cards()
    populate_comments()

if __name__ == '__main__':
    export_favro()