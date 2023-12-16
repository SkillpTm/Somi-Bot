####################################################################################################

import sqlite3

####################################################################################################

from lib.db_modules.CommonDB import CommonDB



class FeedbackDB(CommonDB):

    def __init__(self) -> None:
        super().__init__(database_path = "../../storage/db/feedback.db",
                         table_name = "feedback",
                         table_structure = """(server_id text,
                                               user_id text,
                                               user_name text,
                                               submission_time text,
                                               feedback text)""")

    ####################################################################################################

    def submit(self, server_id: int, user_id: int, user_name: str, submission_time: str, feedback: str) -> None:
        """This function submits feedback to the db"""

        conn = sqlite3.connect(self.database_path)
        c = conn.cursor()

        c.execute(f"INSERT INTO {self.table_name} VALUES ('{server_id}', '{user_id}', '{user_name}', '{submission_time}', '{feedback}')")

        conn.commit()

        conn.close()