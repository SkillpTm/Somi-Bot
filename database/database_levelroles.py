import sqlite3
import os

database_path = os.path.join(os.path.dirname(__file__), '../storage/db/levelroles.db')

###check#db###########################################################

def check_levelroles_for_server_role_and_level(server_id: int, role_id: int = None, level: int = None) -> bool:
    conn = sqlite3.connect(database_path)
    c = conn.cursor()

    c.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='server{server_id}'")

    if c.fetchone() == None :
        c.execute(f"""CREATE TABLE server{server_id} (role_id text,
                                                      level integer)""")

        conn.commit()

    if role_id:
        c.execute(f"SELECT role_id FROM server{server_id} WHERE role_id='{role_id}'")

        if c.fetchone() != None :
            return True

    if level != None:
        c.execute(f"SELECT level FROM server{server_id} WHERE level='{level}'")

        if c.fetchone() != None :
            return True

    conn.close()

    return False

###add#role#to#level###########################################################

def add_role_to_level(server_id: int, role_id: int, level: int) -> None:
    conn = sqlite3.connect(database_path)
    c = conn.cursor()

    c.execute(f"""INSERT INTO server{server_id} VALUES ('{role_id}',
                                                        '{level}')""")

    conn.commit()

    conn.close()

###delete#level#role###########################################################

def delete_level_role(server_id: int, role_id: int) -> None:
    conn = sqlite3.connect(database_path)
    c = conn.cursor()

    c.execute(f"DELETE from server{server_id} WHERE role_id = '{role_id}'")

    conn.commit()

    conn.close()

###get#server#roles#and#levels###########################################################

def get_server_level_roles(server_id: int) -> list[list[tuple[str, int]]]:
    conn = sqlite3.connect(database_path)
    c = conn.cursor()

    c.execute(f"SELECT * FROM server{server_id} ORDER BY level ASC")

    levels_and_roles = c.fetchall()
    levelroles = []

    for tuple in levels_and_roles:
        levelroles.append(list(tuple))

    conn.close()

    return levelroles