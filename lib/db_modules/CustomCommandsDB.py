from lib.db_modules.CommonDB import CommonDB



class CustomCommandsDB(CommonDB):

    def __init__(self,
                 server_id: int) -> None:
        super().__init__(database_path = "../../storage/db/custom_commands.db",
                         table_name = f"server{server_id}",
                         table_structure = """(name text,
                                               text text)""")

    ####################################################################################################
        
    def add(self,
            name: str,
            text: str) -> bool:
        """adds the command to the table"""

        inserted = self._insert(select_column = "name",
                                where_column = "name",
                                check_value = name,
                                values = [name, text])
        
        self._close(commit = inserted)

        return inserted

    ####################################################################################################
        
    def delete(self,
               name: str) -> str:
        """deletes the command from the table"""        

        text: list[str] = self._get(select_column = "text",
                                    where_column = "name",
                                    check_value = name)

        deleted = self._delete(select_column = "name",
                               where_column = "name",
                               check_value = name)

        self._close(commit = deleted)

        if not deleted:
            return ""
        else:
            return text[0]

    ####################################################################################################
        
    def get_text(self,
                 name: str) -> str:
        """get the output text for a command"""

        text: list[str] = self._get(select_column = "text",
                                    where_column = "name",
                                    check_value = name)
        
        self._close(commit = False)

        if not text:
            return ""
        else:
            return text[0]

    ####################################################################################################

    def get_list(self) -> list:
        """get all commandnames for the server"""

        command_list = self._get(select_column = "name",
                                 order_column = "name",
                                 order_type = "ASC")
        
        self._close(commit = False)

        return command_list