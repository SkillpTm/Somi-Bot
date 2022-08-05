import sqlite3
import os

###bugs###########################################################

def submit_bug_report(server_id, user_id, user_name, submission_time, bug_report):
    database_path = os.path.join(os.path.dirname(__file__), '../storage/db/bugs_suggestions.db')
    conn = sqlite3.connect(database_path)

    c = conn.cursor()

    c.execute(f"INSERT INTO bugs VALUES ('{server_id}', '{user_id}', '{user_name}', '{submission_time}', '{bug_report}')")

    conn.commit()

    conn.close()

###suggestions###########################################################

def submit_suggestion(server_id, user_id, user_name, submission_time, suggestion):
    database_path = os.path.join(os.path.dirname(__file__), '../storage/db/bugs_suggestions.db')
    conn = sqlite3.connect(database_path)

    c = conn.cursor()

    c.execute(f"INSERT INTO suggestions VALUES ('{server_id}', '{user_id}', '{user_name}', '{submission_time}', '{suggestion}')")

    conn.commit()

    conn.close()