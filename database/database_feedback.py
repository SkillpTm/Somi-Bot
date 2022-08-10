import sqlite3
import os

###bugs###########################################################

def submit_feedback(server_id, user_id, user_name, submission_time, feedback):
    database_path = os.path.join(os.path.dirname(__file__), '../storage/db/feedback.db')
    conn = sqlite3.connect(database_path)

    c = conn.cursor()

    c.execute(f"INSERT INTO feedback VALUES ('{server_id}', '{user_id}', '{user_name}', '{submission_time}', '{feedback}')")

    conn.commit()

    conn.close()