import sqlite3
from typing import Union

class Database:



    def __init__(self, database_file: str, table_name: str):
        self.db = sqlite3.connect(
            database = database_file,
            check_same_thread=False
        )
        self.cur = self.db.cursor()
        self.table_name = table_name



    async def get_data(self, column_to_search: list, content_of_column: list):
        cur = self.cur
        table_name = self.table_name

        COMMAND = f"SELECT * FROM {table_name} WHERE "

        bind = tuple(content_of_column)

        # Check
        if '' in content_of_column or '' in column_to_search:
            return None
        if type(column_to_search) != list or type(content_of_column) != list:
            return None
        if len(column_to_search) != len(content_of_column) or len(column_to_search) <= 0:
            return None

        # Create COMMAND
        for i in range(0, len(column_to_search)):
            COMMAND += f"{column_to_search[i]}=?"
            if i != len(column_to_search) - 1:
                COMMAND += " AND "

        # Exec command
        try:
            cur.execute(COMMAND, bind)
        except sqlite3.OperationalError as error:
            return error
        return cur.fetchall()

        

    async def insert_data(self, columns: list, values: list):
        table_name = self.table_name
        COMMAND = "INSERT INTO {}(".format(table_name)
        COMMAND2 = ") VALUES ("
        bind = tuple(values)

        # Check
        if '' in columns or '' in values:
            return None
        if type(columns) != list or type(values) != list:
            return None
        if len(columns) != len(values) or len(values) <= 0:
            return None
        
        # Create COMMAND
        for i in range(0, len(columns)):
            COMMAND += columns[i]
            COMMAND2 += '?'
            if i != len(columns) - 1:
                COMMAND += ','
                COMMAND2 += ','
        
        COMMAND += COMMAND2
        COMMAND += ')'

        # Exec COMMAND
        try:
            self.cur.execute(COMMAND, bind)
            self.db.commit()
        except sqlite3.OperationalError as error:
            return error
        return True



    async def delete_data(self, column_name: list, content_of_column: str):
        table_name = self.table_name
        db = self.db
        cur = self.cur
        COMMAND = f"DELETE FROM {table_name} WHERE "
        bind = tuple(content_of_column)

        # Check
        if '' in content_of_column or '' in column_name:
            return None
        if type(column_name) != list or type(content_of_column) != list:
            return None
        if len(column_name) != len(content_of_column) or len(column_name) <= 0:
            return None

        # Creating COMMAND
        for i in range(0, len(column_name)):
            COMMAND += f"{column_name[i]}=?"
            if i != len(column_name) - 1:
                COMMAND += " AND "
        
        # Exec COMMAND
        try:
            cur.execute(COMMAND, bind)
            db.commit()
        except sqlite3.OperationalError as error:
            return error
        return True



    async def update_data(
        self, 
        column_to_change: list, 
        content_of_column: list, 
        column_to_search: list, 
        content_of_column_search: list):

        table_name = self.table_name
        cur = self.cur
        db = self.db
        ctc = column_to_change
        coc = content_of_column
        cts = column_to_search
        cocs = content_of_column_search

        COMMAND = f"UPDATE {table_name} SET "
        COMMAND2 = "WHERE "

        # Check

        if '' in ctc or '' in coc or '' in cts or '' in cocs:
            return None
        if type(ctc) != list or type(coc) != list or type(cts) != list or type(cocs) != list:
            return None
        if len(ctc) != len(coc) or len(coc) <= 0:
            return None
        if len(cts) != len(cocs) or len(cocs) <= 0:
            return None

        # Create COMMAND
        for i in range(0, len(ctc)):
            COMMAND += f"{ctc[i]}=? "
            if i != len(ctc) - 1:
                COMMAND += ', '
        
        for i in range(0, len(cts)):
            COMMAND2 += f"{cts[i]}=?"
            if i != len(cts) - 1:
                COMMAND2 += ' AND '
        
        COMMAND += COMMAND2

        # Create bind variable
        bind1 = tuple(content_of_column)
        bind2 = tuple(content_of_column_search)
        bind = bind1 + bind2

        # Exec COMMAND
        try:
            cur.execute(COMMAND, bind)
            db.commit()
        except sqlite3.OperationalError as error:
            return error

        return True

    async def execute(self, COMMAND: str, bind: Union[tuple, str] = None):
            db = self.db
            cur = self.cur
            if bind == None:
                try:
                    cur.execute(COMMAND)
                    db.commit()
                    return cur.fetchall()
                except sqlite3.OperationalError as error:
                    return error
            elif type(bind) == tuple:
                try:
                    cur.execute(COMMAND, bind)
                    db.commit()
                    return cur.fetchall()
                except sqlite3.OperationalError as error:
                    return error
            else:
                raise TypeError(f"bind type must tuple, got {type(bind)}")