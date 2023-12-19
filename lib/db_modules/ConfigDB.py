####################################################################################################

import nextcord

####################################################################################################

from lib.db_modules.CommonDB import CommonDB



class ConfigDB(CommonDB):

    def __init__(self,
                 server_id: int,
                 config_type: str) -> None:
        self.config_type = config_type

        super().__init__(database_path = "../../storage/db/config.db",
                         table_name = f"server{server_id}",
                         table_structure = """(type text,
                                               data_1 text,
                                               data_2 text)""")

    ####################################################################################################

    def add(self,
            data_1: str | int,
            data_2 = "") -> bool:
        """adds the role/channel id to the config db"""

        in_table = False

        if any(element == self.config_type for element in ["AuditLogChannel", "DefaultRole"]): # these 2 can only exist once, so we check against the type
            in_table = self._check_if_in_table(select_column = "type",
                                               where_column = "type",
                                               check_value = self.config_type)

        else: # the rest of the config_types can have multiple vales, so we check for the id at data_1
            in_table_temp = self._check_if_in_table(select_column = "type",
                                                    where_column = "data_1",
                                                    check_value = data_1)

            if in_table_temp:
                values = self._get(select_column = "type",
                                   where_column = "data_1",
                                   check_value = data_1,
                                   multiple_columns = True,
                                   multiple_columns_and_rows=True)

                if [element[0] for element in values if self.config_type == element[0]]:
                    in_table = True
                else:
                    in_table = False

            else:
                in_table = False

        if self.config_type == "LevelRoles": # LevelRoles need to be checked for, if the level already exists, aswell as the id
            in_table = self._check_if_in_table(select_column = "data_2",
                                               where_column = "data_2",
                                               check_value = data_2)
            
        if in_table:
            self._close(commit = False)

            return False

        inserted = self._insert(values = [self.config_type, data_1, data_2])
        
        self._close(commit = inserted)

        return inserted

    ####################################################################################################

    def delete(self,
               data_1: str | int) -> bool:
        """deletes the role/channel id from the db"""

        in_table = False

        if any(element == self.config_type for element in ["AuditLogChannel", "DefaultRole"]): # these 2 can only exist once, so we check against the type
            in_table = self._check_if_in_table(select_column = "type",
                                               where_column = "type",
                                               check_value = self.config_type)

        else: # the rest of the config_types can have multiple vales, so we check for the id at data_1
            in_table_temp = self._check_if_in_table(select_column = "type",
                                                    where_column = "data_1",
                                                    check_value = data_1)

            if in_table_temp:
                values = self._get(select_column = "type",
                                   where_column = "data_1",
                                   check_value = data_1,
                                   multiple_columns = True,
                                   multiple_columns_and_rows=True)

                if [element[0] for element in values if self.config_type == element[0]]:
                    in_table = True
                else:
                    in_table = False

            else:
                in_table = False
            
        if not in_table:
            self._close(commit = False)

            return False

        deleted = self._delete(where_column = "data_1",
                               check_value = data_1,
                               where_column2 = "type",
                               check_value2 = self.config_type)
        
        self._close(commit = deleted)

        return deleted

    ####################################################################################################

    async def get_list(self,
                       *,
                       server: nextcord.Guild) -> list[str] | list[list[str, str]]: # Make output
        """gets a list of all channel/role ids or a list of lists with the LevelRoles ids and the levels"""

        if self.config_type != "LevelRoles":
            select_column = "data_1"
            multiple_columns = False
            multiple_columns_and_rows = False
        else:
            select_column = "data_1, data_2"
            multiple_columns = True
            multiple_columns_and_rows = True

        ids: list[str] | list[list[str, str]] = self._get(select_column = select_column,
                                                          where_column = "type",
                                                          check_value = self.config_type,
                                                          multiple_columns = multiple_columns,
                                                          multiple_columns_and_rows = multiple_columns_and_rows)

        self._close(commit = False)

        if any(element == self.config_type for element in ["AuditLogChannel", "HiddenChannels", "LevelIgnoreChannels"]):
            for id in ids:
                if not server.get_channel(int(id)):
                    self.delete(id)
                    ids.remove(id)

        elif self.config_type == "DefaultRole":
            for id in ids:
                if not server.get_role(int(id)):
                    self.delete(id)
                    ids.remove(id)

        elif self.config_type == "LevelRoles":
            for id_level in ids:
                if not server.get_role(id_level[0]):
                    from lib.modules.LevelRoles import LevelRoles

                    await LevelRoles().remove_from_members(server, server.get_role(id_level[0]))
                    self.delete(id_level)
                    ids.remove(id_level)

        return ids