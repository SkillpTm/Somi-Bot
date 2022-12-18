####################################################################################################

import os
import sqlite3
import time
import random

####################################################################################################



class LevelsDB():

    def __init__(self) -> None:
        self.database_path = os.path.join(os.path.dirname(__file__), '../../storage/db/levels.db')

    ####################################################################################################

    @staticmethod
    def calulate_level(total_xp: int) -> tuple[int, int]:
        """
        This is the formular to calculate someone's level. Every level has 200xp more than the last one (Level 1 has 300 xp)
        Meaning that the formular to get how much xp a level requires is: ((level - 1) * 200) + 300
        To calculation for your level from your xp is: ((XP - 300) / 200) + 1
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

    def create_table(self,
                     server_id: int) -> None:
        """Creates a table, if there isn't one already"""

        conn = sqlite3.connect(self.database_path)
        c = conn.cursor()

        c.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='server{server_id}'")

        if not c.fetchone():
            c.execute(f"""CREATE TABLE server{server_id} (user_id text,
                                                          message_count integer,
                                                          total_xp integer,
                                                          cooldown_time integer)""")

            conn.commit()

        conn.close()

    ####################################################################################################

    def insert_user(self,
                    server_id: int,
                    user_id: int) -> None:
        """Inserts a user into the levels db, if they aren't already"""

        self.create_table(server_id)

        conn = sqlite3.connect(self.database_path)
        c = conn.cursor()

        c.execute(f"SELECT user_id FROM server{server_id} WHERE user_id='{user_id}'")

        if not c.fetchone():
            c.execute(f"""INSERT INTO server{server_id} VALUES ('{user_id}',
                                                                '0',
                                                                '0',
                                                                '0')""")

            conn.commit()

        conn.close()

    ####################################################################################################

    def increase_user_xp(self,
                         server_id: int,
                         user_id: int) -> None:
        """Increases the message count, total xp and sets the cooldown of a user"""

        self.create_table(server_id)

        conn = sqlite3.connect(self.database_path)
        c = conn.cursor()

        c.execute(f"SELECT * FROM server{server_id} WHERE user_id='{user_id}'")

        user_data = c.fetchone()
        message_count: int = user_data[1] + 1
        total_xp: int = user_data[2] + random.choice(range(10, 15))
        cooldown_time: int = int(time.time()) + random.choice(range(55, 65))

        c.execute(f"UPDATE server{server_id} SET message_count='{message_count}', total_xp='{total_xp}', cooldown_time={cooldown_time} WHERE user_id='{user_id}'")

        conn.commit()

        conn.close()

    ####################################################################################################

    def get_user_cooldown(self,
                          server_id: int,
                          user_id: int) -> int:
        """Returns the cooldown of a user form the db"""

        self.create_table(server_id)

        conn = sqlite3.connect(self.database_path)
        c = conn.cursor()

        c.execute(f"SELECT cooldown_time FROM server{server_id} WHERE user_id='{user_id}'")

        cooldown_time: int = c.fetchone()[0]

        conn.close()

        return cooldown_time

    ####################################################################################################

    def get_user_level(self,
                       server_id: int,
                       user_id: int) -> tuple[int, int]:
        """Calulates the level of a user and returns it with their id"""

        self.create_table(server_id)

        conn = sqlite3.connect(self.database_path)
        c = conn.cursor()

        c.execute(f"SELECT total_xp FROM server{server_id} WHERE user_id='{user_id}'")

        user_level, xp_until_next_level = LevelsDB().calulate_level(c.fetchone()[0])

        return user_level, xp_until_next_level

    ####################################################################################################

    def get_user_rank(self,
                      server_id: int,
                      user_id: int) -> int:
        """Gets the rank of a user on the server"""

        self.create_table(server_id)

        conn = sqlite3.connect(self.database_path)
        c = conn.cursor()

        c.execute(f"SELECT * FROM (SELECT user_id, ROW_NUMBER() OVER (ORDER BY total_xp DESC) FROM server{server_id}) WHERE user_id='{user_id}'")

        user_and_rank = c.fetchone()

        return user_and_rank[1]


    ####################################################################################################

    def get_all_user_levels(self,
                            server_id: int,
                            limit: int = 10_000_000) -> list[list[tuple[int, int]]]:
        """Returns all users with their levels in a list"""

        self.create_table(server_id)

        conn = sqlite3.connect(self.database_path)
        c = conn.cursor()

        c.execute(f"SELECT user_id, total_xp FROM server{server_id} ORDER BY total_xp DESC LIMIT {limit}")

        xp_and_ids = c.fetchall()
        user_ids_and_levels = []

        for tuple_xp_and_id in xp_and_ids:
            current_user = list(tuple_xp_and_id)

            user_level, xp_until_next_level = LevelsDB().calulate_level(current_user[1])

            user_ids_and_levels.append([int(current_user[0]), user_level])

        return user_ids_and_levels