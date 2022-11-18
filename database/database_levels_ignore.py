import os
import sqlite3

database_path = os.path.join(os.path.dirname(__file__), '../storage/db/levels_ignore.db')

###make#ignore#channel#table###########################################################

def make_ignore_channel_table(server_id: int) -> None:
    conn = sqlite3.connect(database_path)
    c = conn.cursor()

    c.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='server{server_id}'")

    if c.fetchone() == None :
        c.execute(f"CREATE TABLE server{server_id} (channel_id text)")

        conn.commit()

    conn.close()

###ignore#channel###########################################################

def ignore_channel(server_id: int, channel_id: int) -> bool:
    conn = sqlite3.connect(database_path)
    c = conn.cursor()

    c.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='server{server_id}'")

    if c.fetchone() == None :
        c.execute(f"CREATE TABLE server{server_id} (channel_id text)")

        conn.commit()

    c.execute(f"SELECT channel_id FROM server{server_id} WHERE channel_id='{channel_id}'")

    if c.fetchone() == None :
        c.execute(f"INSERT INTO server{server_id} VALUES ('{channel_id}')")

        conn.commit()

        conn.close()

        return True

    c.execute(f"DELETE from server{server_id} WHERE channel_id = '{channel_id}'")

    conn.close()

    return False

###ignore#channels#list###########################################################

def ignore_channels_list(server_id: int) -> list[int]:
    conn = sqlite3.connect(database_path)
    c = conn.cursor()

    c.execute(f"SELECT * FROM server{server_id}")

    ignore_channel_tuple = c.fetchall()
    ignore_channel_ids = []

    for channel in ignore_channel_tuple:
        ignore_channel_ids.append(int(channel[0]))

    conn.close()

    return ignore_channel_ids