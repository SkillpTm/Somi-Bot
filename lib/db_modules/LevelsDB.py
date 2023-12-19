####################################################################################################

import time
import random

####################################################################################################

from lib.db_modules.CommonDB import CommonDB



class LevelsDB(CommonDB):

    def __init__(self,
                 server_id: int) -> None:
        super().__init__(database_path = "../../storage/db/levels.db",
                         table_name = f"server{server_id}",
                         table_structure = """(user_id text,
                                               message_count integer,
                                               total_xp integer,
                                               cooldown integer)""")

    ####################################################################################################

    @staticmethod
    def calulate_level(total_xp: int) -> tuple[int, int]:
        """
        This is the formular to calculate someone's level. Every level has 200xp more than the last one (Level 1 has 300 xp)
        Meaning that the formular to get how much xp a level requires is: ((level - 1) * 200) + 300
        To formular for your level from your xp is: ((XP - 300) / 200) + 1
        """

        user_level: int = 0
        current_level_xp_needed: int = 300

        while total_xp > 0:
            user_level += 1
            total_xp -= current_level_xp_needed
            current_level_xp_needed += 200

        xp_until_next_level = total_xp * (-1)

        return user_level, xp_until_next_level

    ####################################################################################################

    def add(self,
            user_id: int) -> None:
        """adds a user to the table, but notably DOESN'T commit"""

        inserted = self._insert(select_column = "user_id",
                                where_column = "user_id",
                                check_value = user_id,
                                values = [str(user_id), 0, 0, 0])


    ####################################################################################################

    def increase_xp(self,
                         user_id: int) -> None:
        """increase the user's xp, their messages count and their cooldown"""

        self.add(user_id)

        user_data = self._get(select_column = "*",
                              where_column = "user_id",
                              check_value = str(user_id),
                              multiple_columns = True)

        message_count: int = user_data[1] + 1
        total_xp: int = user_data[2] + random.choice(range(10, 15))
        cooldown: int = int(time.time()) + random.choice(range(55, 65))

        self.cur.execute(f"""UPDATE {self.table_name}
                             SET message_count='{message_count}', total_xp='{total_xp}', cooldown={cooldown}
                             WHERE user_id='{user_id}'""")

        self._close(commit = True)

    ####################################################################################################

    def get_cooldown(self,
                          user_id: int) -> int:
        """gtes the user's cooldown"""

        self.add(user_id)

        cooldown = self._get(select_column = "cooldown",
                             where_column = "user_id",
                             check_value = str(user_id))
        
        self._close(commit = True)
        
        return cooldown[0]

    ####################################################################################################

    def get_level(self,
                       user_id: int) -> tuple[int, int]:
        """get the user's level and the xp required until their next level"""

        self.add(user_id)

        total_xp = self._get(select_column = "total_xp",
                             where_column = "user_id",
                             check_value = str(user_id))
        
        self._close(commit = True)
        
        if not total_xp:
            total_xp = 0 
        else:
            total_xp = total_xp[0]

        return self.calulate_level(total_xp)

    ####################################################################################################

    def get_rank(self,
                      user_id: int) -> int:
        """get the leaderboard position of the user in this server"""

        self.add(user_id)

        self.cur.execute(f"""SELECT row_num
                             FROM (
                                 SELECT user_id,
                                     ROW_NUMBER() OVER (ORDER BY total_xp DESC) AS row_num
                                 FROM {self.table_name}
                             )
                             WHERE user_id='{user_id}'""")

        rank = self.cur.fetchone()[0]

        self._close(commit = True)

        return rank


    ####################################################################################################

    def get_all_user_levels(self,
                            limit: int = 10_000_000) -> list[list[tuple[int, int]]]:
        """get a list of lists with user ids and their levels, sorted by most xp"""

        self.cur.execute(f"""SELECT user_id, total_xp
                             FROM {self.table_name}
                             ORDER BY total_xp DESC
                             LIMIT {limit}""")

        ids_and_xp: list[tuple[str, int]] = self.cur.fetchall()
        ids_and_levels = []

        for current_user in ids_and_xp:
            current_user = list(current_user)

            user_level, xp_until_next_level = self.calulate_level(current_user[1])

            ids_and_levels.append([int(current_user[0]), user_level])

        self._close(commit = False)

        return ids_and_levels