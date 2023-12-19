####################################################################################################

from lib.db_modules.CommonDB import CommonDB



class FeedbackDB(CommonDB):

    def __init__(self) -> None:
        super().__init__(database_path = "../../storage/db/feedback.db",
                         table_name = "feedback",
                         table_structure = """(server_id text,
                                               user_id text,
                                               username text,
                                               time text,
                                               text text)""")
        
    ####################################################################################################
        
    def add(self, 
            server_id: int,
            user_id: int,
            username: str,
            time: str,
            text: str) -> None:
        """add the feedbaack to the db"""

        inserted = self._insert(values = [server_id, user_id, username, time, text])

        self._close(commit = inserted)