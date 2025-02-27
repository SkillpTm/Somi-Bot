from lib.db_modules.CommonDB import CommonDB



class KeywordDB(CommonDB):

    def __init__(self,
                 server_id: int,
                 user_id: int) -> None:
        self.first_part_table_name = f"server{server_id}"

        super().__init__(database_path = "../../storage/db/user_data/keywords.db",
                         table_name = f"server{server_id}_user{user_id}",
                         table_structure = """(keyword text)""")

    ####################################################################################################

    def add(self,
            keyword: str) -> bool:
        """adds the keyword to the table"""

        inserted = self._insert(select_column = "keyword",
                                where_column = "keyword",
                                check_value = keyword,
                                values = [keyword])
        
        self._close(commit = inserted)
        
        return inserted

    ####################################################################################################

    def delete(self,
               keyword: str) -> bool:
        """deletes the keyword from the table"""

        deleted = self._delete(select_column = "keyword",
                               where_column = "keyword",
                               check_value = keyword)
        
        self._close(commit = deleted)

        return deleted

    ####################################################################################################

    def delete_all(self) -> None:
        """drops the table with the keywords"""

        self._drop()
        self._close(commit = True)

    ####################################################################################################

    def get_list(self) -> list[str]:
        """gets a list with all keywords of the user"""

        keywords = self._get(select_column = "keyword",
                             order_column = "keyword",
                             order_type = "ASC")
        
        self._close(commit = False)

        return keywords

    ####################################################################################################

    def get_all(self) -> dict[int, list[str]]:
        """gets all users with their keywords from this server, except for the provided user and their keywords"""

        self.cur.execute(f"""SELECT name
                             FROM sqlite_master
                             WHERE type='table'
                                 AND name LIKE '{self.first_part_table_name}%'
                             EXCEPT SELECT name
                             FROM sqlite_master
                             WHERE name = '{self.table_name}'""")
        
        all_user_table_names: list[tuple[str]] = self.cur.fetchall()
        all_users_keywords: dict[int, list[str]] = {}

        for user in all_user_table_names:
            user = user[0]
            
            self.cur.execute(f"""SELECT keyword
                                    FROM {user}
                                    ORDER BY keyword ASC""")
            
            user_keywords: list[tuple[str]] = self.cur.fetchall()
            user_keywords = [keyword[0] for keyword in user_keywords]

            if not user_keywords:
                continue

            underscore_position = user.find("_")
            user_id = int(user[underscore_position+5:])

            all_users_keywords.update({user_id: user_keywords})

        self._close(commit = False)

        return all_users_keywords