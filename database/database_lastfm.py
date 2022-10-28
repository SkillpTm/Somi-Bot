import sqlite3
import os

###lastfm#check###########################################################

def lastfm_get_user_from_db(user_id):
    database_path = os.path.join(os.path.dirname(__file__), '../storage/db/lastfm.db')
    conn = sqlite3.connect(database_path)

    c = conn.cursor()

    c.execute(f"SELECT lastfm_username FROM lastfmUsers WHERE discord_user_id = {str(user_id)}")

    tuple_lastfm_username = c.fetchone()

    if tuple_lastfm_username == None:
        conn.close()
        return False

    for username in tuple_lastfm_username:
        lastfm_username = username

    conn.close()
    return lastfm_username

###lastfm#set###########################################################

def lastfm_set_user(user_id, lastfm_username):
    database_path = os.path.join(os.path.dirname(__file__), '../storage/db/lastfm.db')
    conn = sqlite3.connect(database_path)

    c = conn.cursor()

    c.execute(f"INSERT INTO lastfmUsers VALUES ('{str(user_id)}', '{lastfm_username}')")

    conn.commit()

    conn.close()