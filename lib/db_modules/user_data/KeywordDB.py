import sqlite3
import os

###keyword#add###########################################################

def create_keyword(user_id, clean_keyword):
    database_path = os.path.join(os.path.dirname(__file__), '../storage/db/keywords.db')
    conn = sqlite3.connect(database_path)

    c = conn.cursor()

    c.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='user{user_id}'")

    if c.fetchone() != None :
        pass
    else:
        c.execute(f"CREATE TABLE user{user_id} (keywords text)")

        conn.commit()

    c.execute(f"SELECT keywords FROM user{user_id}")
    tuple_all_keywords = c.fetchall()
    all_keywords = []

    for keywords in tuple_all_keywords:
        all_keywords.append(keywords[0])

    if clean_keyword in all_keywords:
        conn.close()
        return False

    c.execute(f"INSERT INTO user{user_id} VALUES ('{clean_keyword}')")

    conn.commit()

    conn.close()
    return True

###keyword#delete###########################################################

def delete_keyword(user_id, clean_keyword):
    database_path = os.path.join(os.path.dirname(__file__), '../storage/db/keywords.db')
    conn = sqlite3.connect(database_path)

    c = conn.cursor()

    if clean_keyword == "ALL":
        conn.close()
        return "ALL"

    c.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='user{user_id}'")

    if c.fetchone() == None :
        conn.close()
        return False

    c.execute(f"SELECT keywords FROM user{user_id}")
    tuple_all_keywords = c.fetchall()
    all_keywords = []

    for keywords in tuple_all_keywords:
        all_keywords.append(keywords[0])

    if not clean_keyword in all_keywords:
        conn.close()
        return False

    c.execute(f"DELETE from user{user_id} WHERE keywords = '{clean_keyword}'")

    conn.commit()

    conn.close()
    return True

###keyword#delete#ALL###########################################################

def delete_all_user_keywords(user_id):
    database_path = os.path.join(os.path.dirname(__file__), '../storage/db/keywords.db')
    conn = sqlite3.connect(database_path)

    c = conn.cursor()
    try:
        c.execute(f"SELECT COUNT(*) FROM user{user_id}")
        if c.fetchone() != (0,):
            user_has_a_table_thats_not_zero = True
        else:
            int("go to except")
    except:
        user_has_a_table_thats_not_zero = False
        pass

    if user_has_a_table_thats_not_zero:
        c.execute(f"DROP TABLE user{user_id}")
        conn.commit()

        conn.close()
        return True

    conn.commit()

    conn.close()
    return False

###keyword#list###########################################################

def list_keyword(user_id):
    database_path = os.path.join(os.path.dirname(__file__), '../storage/db/keywords.db')
    conn = sqlite3.connect(database_path)

    c = conn.cursor()

    c.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='user{user_id}'")

    if c.fetchone() == None :
        conn.close()
        return []

    c.execute(f"SELECT keywords FROM user{user_id} ORDER BY keywords ASC")
    all_keywords = c.fetchall()

    keywords_list = []

    for keyword in all_keywords:
        keywords_list.append(keyword[0])

    conn.close()
    return keywords_list

###keyword############################################################

def get_keywords(message_author_id):
    database_path = os.path.join(os.path.dirname(__file__), '../storage/db/keywords.db')
    conn = sqlite3.connect(database_path)

    c = conn.cursor()

    c.execute(f"""SELECT name FROM sqlite_master WHERE type='table'
                  EXCEPT SELECT name FROM sqlite_master WHERE name = 'user{message_author_id}'""")
    all_user_tables = c.fetchall()
    all_users_keywords = {}

    for user in all_user_tables:
        this_user_keywords = []
        clean_user = user[0]

        c.execute(f"SELECT keywords FROM {user[0]} ORDER BY keywords ASC")
        tuple_user_keywords = c.fetchall()

        for keyword in tuple_user_keywords:
            this_user_keywords.append(keyword[0])

        all_users_keywords.update({clean_user[4:]: this_user_keywords})

    conn.close()
    return all_users_keywords