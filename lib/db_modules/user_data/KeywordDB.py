####################################################################################################

import os
import sqlite3

####################################################################################################



class KeywordDB():

    def __init__(self) -> None:
        self.database_path = os.path.join(os.path.dirname(__file__), '../../../storage/db/user_data/keywords.db')

    ####################################################################################################

    def create_table(self,
                     server_id: int,
                     user_id: int) -> None:
        """Creates a table, if there isn't one already"""

        conn = sqlite3.connect(self.database_path)
        c = conn.cursor()

        c.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='server{server_id}_user{user_id}'")

        if not c.fetchone():
            c.execute(f"CREATE TABLE server{server_id}_user{user_id} (keyword text)")

            conn.commit()

        conn.close()

    ####################################################################################################

    def add(self,
            server_id: int,
            user_id: int,
            keyword: str) -> bool:
        """This function will add a keyword to a user's table"""

        self.create_table(server_id, user_id)
        
        conn = sqlite3.connect(self.database_path)
        c = conn.cursor()

        c.execute(f"SELECT keyword FROM server{server_id}_user{user_id} WHERE keyword = '{keyword}'")

        if c.fetchone():
            conn.close()
            return False

        c.execute(f"INSERT INTO server{server_id}_user{user_id} VALUES ('{keyword}')")

        conn.commit()

        conn.close()
        return True

    ####################################################################################################

    def delete(self,
               server_id: int,
               user_id: int,
               keyword: str) -> bool | str:
        """This function deletes a keyword from the user's table. If the keyword input is 'ALL', it will immeaditly return back"""
        
        self.create_table(server_id, user_id)

        conn = sqlite3.connect(self.database_path)
        c = conn.cursor()

        if keyword == "ALL":
            conn.close()
            return "ALL"

        c.execute(f"SELECT keyword FROM server{server_id}_user{user_id} WHERE keyword = '{keyword}'")
        
        if not c.fetchone():
            conn.close()
            return False

        c.execute(f"DELETE from server{server_id}_user{user_id} WHERE keyword = '{keyword}'")

        conn.commit()

        conn.close()
        return True

    ####################################################################################################

    def delete_all(self,
                   server_id: int,
                   user_id: int) -> None:
        """This function drops a user's keyword table"""
        
        self.create_table(server_id, user_id)

        conn = sqlite3.connect(self.database_path)
        c = conn.cursor()

        c.execute(f"DROP TABLE server{server_id}_user{user_id}")
        conn.commit()

        conn.close()

    ####################################################################################################

    def user_list(self,
                  server_id: int,
                  user_id: int) -> list[str]:
        """This function returns a list of all the keywords a user has"""
        
        self.create_table(server_id, user_id)

        conn = sqlite3.connect(self.database_path)
        c = conn.cursor()

        c.execute(f"SELECT keyword FROM server{server_id}_user{user_id} ORDER BY keyword ASC")
        all_keywords = c.fetchall()

        user_keywords = [keyword[0] for keyword in all_keywords]

        conn.close()
        return user_keywords

    ####################################################################################################

    def get_all(self,
                message_server_id: int,
                message_author_id: int) -> dict[int, list[str]]:
        """This function returns of a dict with all users on the guild and their keywords"""
        
        self.create_table(message_server_id, message_author_id)

        conn = sqlite3.connect(self.database_path)
        c = conn.cursor()

        c.execute(f"""SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'server{message_server_id}%'
                      EXCEPT SELECT name FROM sqlite_master WHERE name = 'server{message_server_id}_user{message_author_id}'""")
        all_user_tables = c.fetchall()
        all_users_keywords: dict[int, list[str]] = {}

        for user in all_user_tables:
            c.execute(f"SELECT keyword FROM {user[0]} ORDER BY keyword ASC")
            tuple_user_keywords = c.fetchall()
            this_user_keywords: list[str] = [keyword[0] for keyword in tuple_user_keywords]

            if this_user_keywords != []:
                underscore_position = user[0].find("_")
                user_id = int(user[0][underscore_position+5:])

                all_users_keywords.update({user_id: this_user_keywords})

        conn.close()
        return all_users_keywords