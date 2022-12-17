import sqlite3
import os

###get#relevant#history#ids###########################################################

def get_history_ids():
    database_path = os.path.join(os.path.dirname(__file__), '../storage/db/subreddit_history.db')
    conn = sqlite3.connect(database_path)

    c = conn.cursor()

    c.execute(f"SELECT id FROM somi ORDER BY id DESC LIMIT 201")
    tuple_history_ids = c.fetchall()
    history_ids = []

    for id in tuple_history_ids:
        history_ids.append(id[0])

    conn.close()

    return history_ids

###add#post#id#to#db###########################################################

def add_new_id_to_database(new_id):
    database_path = os.path.join(os.path.dirname(__file__), '../storage/db/subreddit_history.db')
    conn = sqlite3.connect(database_path)

    c = conn.cursor()

    c.execute(f"INSERT INTO somi VALUES ('{new_id}')")

    conn.commit()

    conn.close()