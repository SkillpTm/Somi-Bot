from lib.db_modules.CommonDB import CommonDB



class LastFmDB(CommonDB):

    def __init__(self) -> None:
        super().__init__(database_path = "../../storage/db/lastfm.db",
                         table_name = "lastfmUsers",
                         table_structure = """(discord_id text,
                                               lastfm_username text)""")

    ####################################################################################################

    def add(self,
            user_id: int,
            lastfm_username: str) -> bool:
        """add the lastfm username with the discord id in the db"""

        inserted = self._insert(select_column = "lastfm_username",
                                where_column = "discord_id",
                                check_value = str(user_id),
                                values = [user_id, lastfm_username])
        
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
        """get the lastfm username from the user with their discord id"""

        username = self._get(select_column = "lastfm_username",
                             where_column = "discord_id",
                             check_value = str(user_id))

        self._close(commit = False)

        if not username:
            return ""
        else:
            return username[0]