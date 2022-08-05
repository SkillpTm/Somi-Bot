import sqlite3
import os

###custom#add###########################################################

def create_custom_command(server_id, clean_commandname, commandtext):
    database_path = os.path.join(os.path.dirname(__file__), '../storage/db/custom_commands.db')
    conn = sqlite3.connect(database_path)

    c = conn.cursor()

    c.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='server{server_id}'")

    if c.fetchone() != None :
        pass
    else:
        c.execute(f"CREATE TABLE server{server_id} (clean_commandname text, commandtext text)")

        conn.commit()

    c.execute(f"SELECT clean_commandname FROM server{server_id}")
    tuple_all_commandnames = c.fetchall()
    all_commandnames = []

    for commandname in tuple_all_commandnames:
        all_commandnames.append(commandname[0])

    if clean_commandname in all_commandnames:
        conn.close()
        return False

    c.execute(f"INSERT INTO server{server_id} VALUES ('{clean_commandname}', '{commandtext}')")

    conn.commit()

    conn.close()
    return True

###custom#delete###########################################################

def delete_custom_command(server_id, clean_commandname):
    database_path = os.path.join(os.path.dirname(__file__), '../storage/db/custom_commands.db')
    conn = sqlite3.connect(database_path)

    c = conn.cursor()

    c.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='server{server_id}'")

    if c.fetchone() == None:
        conn.close()
        return False, ""

    c.execute(f"SELECT clean_commandname FROM server{server_id}")
    tuple_all_commandnames = c.fetchall()
    all_commandnames = []

    for commandname in tuple_all_commandnames:
        all_commandnames.append(commandname[0])

    if not clean_commandname in all_commandnames:
        conn.close()
        return False, ""

    c.execute(f"SELECT commandtext FROM server{server_id} WHERE clean_commandname = '{clean_commandname}'")
    tuple_commandtext = c.fetchall()
    commandtext = ""

    for command_text in tuple_commandtext:
        commandtext += command_text[0]

    c.execute(f"DELETE from server{server_id} WHERE clean_commandname = '{clean_commandname}'")

    conn.commit()

    conn.close()
    return True, commandtext

###custom#list###########################################################

def list_custom(server_id):
    database_path = os.path.join(os.path.dirname(__file__), '../storage/db/custom_commands.db')
    conn = sqlite3.connect(database_path)

    c = conn.cursor()

    c.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='server{server_id}'")

    if c.fetchone() == None :
        conn.close()
        return 0, []

    c.execute(f"SELECT clean_commandname FROM server{server_id} ORDER BY clean_commandname ASC")
    tuple_all_commandnames = c.fetchall()
    all_commandnames = []

    for commandname in tuple_all_commandnames:
        all_commandnames.append(commandname[0])

    amount = len(all_commandnames)

    conn.close()
    return amount, all_commandnames

###custom#command###########################################################

def command_custom(server_id, clean_commandname):
    database_path = os.path.join(os.path.dirname(__file__), '../storage/db/custom_commands.db')
    conn = sqlite3.connect(database_path)

    c = conn.cursor()

    c.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='server{server_id}'")

    if c.fetchone() == None :
        conn.close()
        return ""

    c.execute(f"SELECT commandtext FROM server{server_id} WHERE clean_commandname = '{clean_commandname}'")
    tuple_commandtext = c.fetchall()
    commandtext = ""

    for command_text in tuple_commandtext:
        commandtext = command_text[0]

    conn.close()
    return commandtext

###custom#command###########################################################

def get_description_custom_command_names(SERVER_ID):
    amount, all_commandnames = list_custom(SERVER_ID)

    if amount == 0:
        return "There are no custom commands"

    output = ", ".join(map(str,all_commandnames))
    
    return output[:99]