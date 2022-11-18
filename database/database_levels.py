import sqlite3
import time
import os
import random

database_path = os.path.join(os.path.dirname(__file__), '../storage/db/levels.db')

###check#db###########################################################

def check_level_for_server_and_user(server_id: int, user_id: int) -> None:
    conn = sqlite3.connect(database_path)
    c = conn.cursor()

    c.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='server{server_id}'")

    if c.fetchone() == None :
        c.execute(f"""CREATE TABLE server{server_id} (user_id text,
                                                      message_count integer,
                                                      total_xp integer,
                                                      cooldown_time integer)""")

        conn.commit()

    c.execute(f"SELECT user_id FROM server{server_id} WHERE user_id='{user_id}'")

    if c.fetchone() == None :
        c.execute(f"""INSERT INTO server{server_id} VALUES ('{user_id}',
                                                            '0',
                                                            '0',
                                                            '0')""")

        conn.commit()

    conn.close()

###get#cooldown###########################################################

def get_user_cooldown(server_id: int, user_id: int) -> int:
    conn = sqlite3.connect(database_path)
    c = conn.cursor()

    c.execute(f"SELECT cooldown_time FROM server{server_id} WHERE user_id='{user_id}'")

    cooldown_time = c.fetchone()[0]

    conn.close()

    return cooldown_time

###increase#user#xp###########################################################

def increase_user_xp(server_id: int, user_id: int) -> None:
    conn = sqlite3.connect(database_path)
    c = conn.cursor()

    c.execute(f"SELECT * FROM server{server_id} WHERE user_id='{user_id}'")

    user_data = c.fetchone()
    message_count = user_data[1] + 1
    total_xp = user_data[2] + random.choice(range(10, 15))
    cooldown_time = int(time.time()) + random.choice(range(55, 65))

    c.execute(f"UPDATE server{server_id} SET message_count='{message_count}', total_xp='{total_xp}', cooldown_time={cooldown_time} WHERE user_id='{user_id}'")

    conn.commit()

    conn.close()

###get#user#level###########################################################

def get_user_level(server_id: int, user_id: int) -> tuple[int, int]:
    conn = sqlite3.connect(database_path)
    c = conn.cursor()

    c.execute(f"SELECT total_xp FROM server{server_id} WHERE user_id='{user_id}'")

    total_xp = c.fetchone()[0]

    user_level = 0
    current_level_xp_needed = 300

    while total_xp > 0:
        user_level += 1
        total_xp -= current_level_xp_needed
        current_level_xp_needed += 200

    xp_until_next_level = total_xp * (-1)

    return user_level, xp_until_next_level

###get#all#user#levels###########################################################

def get_all_user_levels(server_id: int) -> list[list[tuple[int, int]]]:
    conn = sqlite3.connect(database_path)
    c = conn.cursor()

    c.execute(f"SELECT user_id, total_xp FROM server{server_id} ORDER BY total_xp DESC")

    xp_and_ids = c.fetchall()
    user_ids_and_levels = []

    for tuple in xp_and_ids:
        current_user = list(tuple)

        total_xp: int = current_user[1]
        user_level: int = 0
        current_level_xp_needed: int = 300

        while total_xp > 0:
            user_level += 1
            total_xp -= current_level_xp_needed
            current_level_xp_needed += 200

        user_ids_and_levels.append([int(current_user[0]), user_level])

    return user_ids_and_levels