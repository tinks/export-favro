import sqlite3

def setup_db():
    db = sqlite3.connect("local/favro.db")

    cursor = db.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS user (id TEXT NOT NULL PRIMARY KEY, name TEXT, email TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS tag (id TEXT NOT NULL PRIMARY KEY, name TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS collection (id TEXT NOT NULL PRIMARY KEY, name TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS widget (id TEXT NOT NULL PRIMARY KEY, name TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS widget_to_collection (widget_id TEXT NOT NULL, collection_id TEXT NOT NULL)")
    cursor.execute("CREATE TABLE IF NOT EXISTS comment (id TEXT NOT NULL, card_id TEXT NOT NULL, comment TEXT, user_id TEXT, created TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS comment_to_attachment (comment_id TEXT NOT NULL, attachment_url TEXT NOT NULL, name TEXT, new_url TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS custom_field (id TEXT NOT NULL PRIMARY KEY, name TEXT NOT NULL, type TEXT NOT NULL, enabled TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS custom_field_item (id TEXT NOT NULL PRIMARY KEY, custom_field_id TEXT NOT NULL, name TEXT NOT NULL)")
    cursor.execute("CREATE TABLE IF NOT EXISTS card (id TEXT NOT NULL, widget_id TEXT, name TEXT, description TEXT, issue_key INTEGER, start_date TEXT, due_date TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS card_to_tag (card_id TEXT NOT NULL, tag_id TEXT NOT NULL)")
    cursor.execute("CREATE TABLE IF NOT EXISTS card_to_assignment (card_id TEXT NOT NULL, user_id TEXT NOT NULL)")
    cursor.execute("CREATE TABLE IF NOT EXISTS card_to_attachment (card_id TEXT NOT NULL, attachment_url TEXT NOT NULL, name TEXT, new_url TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS card_dependency (from_card_id TEXT NOT NULL, to_card_id TEXT NOT NULL)")
    cursor.execute("CREATE TABLE IF NOT EXISTS card_to_custom_field (card_id TEXT NOT NULL, custom_field_id TEXT NOT NULL, custom_field_blob TEXT)")
    
    db.close()