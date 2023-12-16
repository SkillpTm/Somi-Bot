####################################################################################################

import os
import sqlite3

####################################################################################################

from lib.db_modules.CommonDB import CommonDB



class KeywordDB():

    def __init__(self,
                 server_id: int,
                 user_id: int) -> None:
        self.database_path = os.path.join(os.path.dirname(__file__), '../../../storage/db/user_data/keywords.db')
        
        self.table_name = f"server{server_id}_user{user_id}"
        self.first_part_table_name = f"server{server_id}"
        self.table_structure = """(keyword text)"""

        CommonDB.create_table(self.table_name, self.database_path, self.table_structure)

    ####################################################################################################

    def add(self,
            keyword: str) -> bool:
        """This function will add a keyword to a user's table"""
        
        conn = sqlite3.connect(self.database_path)
        c = conn.cursor()

        c.execute(f"SELECT keyword FROM {self.table_name} WHERE keyword = '{keyword}'")

        if c.fetchone():
            conn.close()
            return False

        c.execute(f"INSERT INTO {self.table_name} VALUES ('{keyword}')")

        conn.commit()

        conn.close()
        return True

    ####################################################################################################

    def delete(self,
               keyword: str) -> bool | str:
        """This function deletes a keyword from the user's table. If the keyword input is 'ALL', it will immeaditly return back"""

        conn = sqlite3.connect(self.database_path)
        c = conn.cursor()

        if keyword == "ALL":
            conn.close()
            return "ALL"

        c.execute(f"SELECT keyword FROM {self.table_name} WHERE keyword = '{keyword}'")
        
        if not c.fetchone():
            conn.close()
            return False

        c.execute(f"DELETE from {self.table_name} WHERE keyword = '{keyword}'")

        conn.commit()

        conn.close()
        return True

    ####################################################################################################

    def delete_all(self) -> None:
        """This function drops a user's keyword table"""

        conn = sqlite3.connect(self.database_path)
        c = conn.cursor()

        c.execute(f"DROP TABLE {self.table_name}")
        conn.commit()

        conn.close()

    ####################################################################################################

    def user_list(self) -> list[str]:
        """This function returns a list of all the keywords a user has"""

        conn = sqlite3.connect(self.database_path)
        c = conn.cursor()

        c.execute(f"SELECT keyword FROM {self.table_name} ORDER BY keyword ASC")
        all_keywords = c.fetchall()

        user_keywords = [keyword[0] for keyword in all_keywords]

        conn.close()
        return user_keywords

    ####################################################################################################

    def get_all(self) -> dict[int, list[str]]:
        """This function returns a dict with all users on the guild and their keywords"""

        conn = sqlite3.connect(self.database_path)
        c = conn.cursor()

        c.execute(f"""SELECT name FROM sqlite_master WHERE type='table' AND name LIKE '{self.first_part_table_name}%'
                      EXCEPT SELECT name FROM sqlite_master WHERE name = '{self.table_name}'""")
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