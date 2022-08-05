import sqlite3
import os

###uses#update###########################################################

def uses_update(table, column_name):
    database_path = os.path.join(os.path.dirname(__file__), '../storage/db/command_uses.db')
    conn = sqlite3.connect(database_path)

    c = conn.cursor()

    c.execute(f"SELECT name FROM {table}")
    tuple_all_column_names = c.fetchall()
    all_column_names = []

    for column in tuple_all_column_names:
        all_column_names.append(column[0])

    if not column_name in all_column_names:
        c.execute(f"INSERT INTO {table} VALUES ('{column_name}', 0)")
        conn.commit()

    c.execute(f"SELECT amount FROM {table} WHERE name = '{column_name}'")
    new_amount = c.fetchone()[0]

    new_amount += 1

    c.execute(f"UPDATE {table} SET amount = '{new_amount}' WHERE name = '{column_name}'")

    conn.commit()

    conn.close()