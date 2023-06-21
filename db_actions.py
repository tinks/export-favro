import sqlite3

def populate_db(query, values):
    db = sqlite3.connect("local/favro.db")

    cursor = db.cursor()
    cursor.executemany(query, values)
    db.commit()

    print(cursor.rowcount, "records inserted")

    db.close()

def request_data(query):
    db = sqlite3.connect("local/favro.db")

    cursor = db.cursor()
    cursor.execute(query)
    data = cursor.fetchall()

    db.close()
    return data