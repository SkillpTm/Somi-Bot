####################################################################################################

import os
import sqlite3

####################################################################################################



class CommonDB():

    def __init__(self,
                 database_path: str,
                 table_name: str,
                 table_structure: str) -> None:
        self.database_path = os.path.join(os.path.dirname(__file__), database_path)

        self.conn = sqlite3.connect(self.database_path)
        self.cur = self.conn.cursor()

        self.table_name = table_name
        self.table_structure = table_structure

        self._create_table()

    ####################################################################################################

    def _close(self,
               *,
               commit: bool) -> None:
        """closes the connection to the db and commits if needed"""

        if commit:
            self.conn.commit()

        self.conn.close()

    ####################################################################################################

    def _create_table(self) -> None:
        """creates the table, if there isn't one already"""

        self.cur.execute(f"""SELECT name
                             FROM sqlite_master
                             WHERE type='table'
                                 AND name='{self.table_name}'""")

        if not self.cur.fetchone():
            self.cur.execute(f"""CREATE TABLE {self.table_name} {self.table_structure}""")

    ####################################################################################################

    def _check_if_in_table(self, 
                           select_column: str,
                           where_column: str,
                           check_value: str) -> bool | list[tuple[str]]:
        """checks if a value is in the table"""

        self.cur.execute(f"""SELECT {select_column}
                             FROM {self.table_name}
                             WHERE {where_column} = '{check_value}'""")

        if self.cur.fetchone():
            return True
        else:
            return False

    ####################################################################################################
    
    def _insert(self,
                *,
                select_column = "",
                where_column = "",
                check_value = "",
                values: list) -> bool:
        """Inserts the inputs provided in that order, if they aren't already in the DB
           You can skip the _check_if_in_table by not providing: select_column | where_column | check_value"""

        if select_column and where_column and check_value:
            if self._check_if_in_table(select_column, where_column, check_value):
                return False

        values = f"({', '.join([f"'{element}'" for element in values])})"

        self.cur.execute(f"""INSERT INTO {self.table_name}
                             VALUES {values}""")

        return True
    
    ####################################################################################################
    
    def _delete(self,
                *,
                select_column = "",
                where_column: str,
                check_value: str,
                where_column2 = "",
                check_value2 = "") -> bool:
        """Deletes the value at the where
           You can skip _check_if_in_table by not providing: select_column"""

        if select_column:
            if not self._check_if_in_table(select_column, where_column, check_value):
                return False
        
        if not where_column2 and not check_value2:
            where2 = ""
        else:
            where2 = f"AND {where_column2} = '{check_value2}'"

        self.cur.execute(f"""DELETE from {self.table_name}
                             WHERE {where_column} = '{check_value}'
                             {where2}""")

        return True
    
    ####################################################################################################
    
    def _get(self,
             *,
             select_column: str,
             where_column = "",
             check_value = "",
             order_column = "",
             order_type = "",
             multiple_columns = False,
             multiple_columns_and_rows = False) -> list:
        """gets the value(s) you asked for, it can also order them and handle multiple values from multiple rows and colums at once"""

        if where_column:
            where = f"WHERE {where_column} = '{check_value}'"
        else:
            where = ""

        if order_column:
            order = f"ORDER BY {order_column} {order_type}"
        else:
            order = ""

        self.cur.execute(f"""SELECT {select_column}
                             FROM {self.table_name}
                             {where}
                             {order}""")

        all_values = self.cur.fetchall()

        if not multiple_columns: # if there is multiple values we don't just want the first tuple value
            all_values = [element[0] for element in all_values]
        elif not multiple_columns_and_rows:
            all_values = [list(element) for element in all_values][0]
        else:
            all_values = [list(element) for element in all_values]

        return all_values
    
    ####################################################################################################
    
    def _drop(self) -> None:
        """dropes the table"""

        self.cur.execute(f"DROP TABLE {self.table_name}")