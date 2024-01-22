####################################################################################################

from lib.db_modules.CommonDB import CommonDB



class WeatherDB(CommonDB):

    def __init__(self) -> None:
        super().__init__(database_path = "../../storage/db/weather.db",
                         table_name = "userLocations",
                         table_structure = """(discord_id text,
                                               location text)""")

    ####################################################################################################

    def add(self,
            user_id: int,
            location: str) -> bool:
        """add the weather location with the discord id in the db"""

        inserted = self._insert(select_column = "location",
                                where_column = "discord_id",
                                check_value = str(user_id),
                                values = [user_id, location])
        
        self._close(commit = inserted)

        return inserted

    ####################################################################################################

    def delete(self,
               user_id: int) -> bool:
        """deletes the user from the db"""

        deleted = self._delete(select_column = "discord_id",
                               where_column = "discord_id",
                               check_value = str(user_id))
        
        self._close(commit = deleted)

        return deleted
    
    ####################################################################################################

    def get(self,
            user_id: int) -> str:
        """get the weather location from the user with their discord id"""

        location = self._get(select_column = "location",
                             where_column = "discord_id",
                             check_value = str(user_id))

        self._close(commit = False)

        if not location:
            return ""
        else:
            return location[0]