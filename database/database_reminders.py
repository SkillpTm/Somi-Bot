import sqlite3
import os

###reminder#add###########################################################

def create_reminder(user_id, reminder_time, bot_reply_link, delete_id, clean_reminder):
    database_path = os.path.join(os.path.dirname(__file__), '../storage/db/reminders.db')
    conn = sqlite3.connect(database_path)

    c = conn.cursor()

    c.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='user{user_id}'")

    if c.fetchone() != None :
        pass
    else:
        c.execute(f"""CREATE TABLE user{user_id} (
                      reminder_time integer,
                      bot_reply_link text,
                      delete_id integer,
                      clean_reminder text
                  )""")

        conn.commit()

    c.execute(f"""INSERT INTO user{user_id}
                  VALUES ('{reminder_time}', '{bot_reply_link}', '{delete_id}', '{clean_reminder}')""")

    conn.commit()

    conn.close()

###reminder#delete###########################################################

def delete_reminder(user_id, delete_id):
    database_path = os.path.join(os.path.dirname(__file__), '../storage/db/reminders.db')
    conn = sqlite3.connect(database_path)

    if delete_id == "ALL":
        conn.close()
        return True, "ALL"

    c = conn.cursor()

    c.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='user{user_id}'")

    if c.fetchone() == None :
        conn.close()
        return False, ""

    c.execute(f"SELECT delete_id FROM user{user_id}")
    delete_ids = c.fetchall()
    all_ids_list = []

    for id in delete_ids:
        all_ids_list.append(id[0])

    if not delete_id in all_ids_list:
        conn.close()
        return False, ""

    c.execute(f"DELETE from user{user_id} WHERE delete_id = '{delete_id}'")

    conn.commit()

    conn.close()
    return True, ""

###reminder#delete#ALL###########################################################

def delete_all_user_reminders(user_id):
    database_path = os.path.join(os.path.dirname(__file__), '../storage/db/reminders.db')
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

###reminder#list###########################################################

def list_reminder(user_id):
    database_path = os.path.join(os.path.dirname(__file__), '../storage/db/reminders.db')
    conn = sqlite3.connect(database_path)

    c = conn.cursor()

    c.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='user{user_id}'")

    if c.fetchone() == None :
        conn.close()
        return 0, [], [], []

    c.execute(f"SELECT * FROM user{user_id}")
    all_reminders = c.fetchall()

    amount = len(all_reminders)
    reminder_times = []
    bot_reply_links = []
    delete_ids = []

    for reminder_time in all_reminders:
        reminder_times.append(reminder_time[0])

    for bot_reply_link in all_reminders:
        bot_reply_links.append(bot_reply_link[1])

    for delete_id in all_reminders:
        delete_ids.append(delete_id[2])

    conn.close()
    return amount, reminder_times, bot_reply_links, delete_ids

###reminder###########################################################

def get_reminder_times():
    database_path = os.path.join(os.path.dirname(__file__), '../storage/db/reminders.db')
    conn = sqlite3.connect(database_path)

    c = conn.cursor()

    c.execute("SELECT name FROM sqlite_master WHERE type='table'")
    all_tables = c.fetchall()
    clean_times = []

    for user in all_tables:
        c.execute(f"SELECT reminder_time FROM {user[0]}")
        all_user_reminder_times = c.fetchall()

        c.execute(f"SELECT delete_id FROM {user[0]}")
        all_user_delete_ids = c.fetchall()

        i = 0

        for time in all_user_reminder_times:
            delete_id = all_user_delete_ids[i]
            i += 1
            clean_user = user[0]
            clean_times.append([clean_user[4:], time[0], delete_id[0]])

    conn.close()
    return clean_times

###reminder###########################################################

def get_reminder_contents(user_id, delete_id):
    database_path = os.path.join(os.path.dirname(__file__), '../storage/db/reminders.db')
    conn = sqlite3.connect(database_path)

    c = conn.cursor()

    c.execute(f"SELECT bot_reply_link FROM user{user_id} WHERE delete_id = '{delete_id}'")
    tuple_bot_reply_link = c.fetchall()
    for link in tuple_bot_reply_link:
        bot_reply_link = link[0]

    c.execute(f"SELECT clean_reminder FROM user{user_id} WHERE delete_id = '{delete_id}'")
    tuple_clean_reminder = c.fetchall()
    for reminder in tuple_clean_reminder:
        clean_reminder = reminder[0]

    conn.close()
    return bot_reply_link, clean_reminder