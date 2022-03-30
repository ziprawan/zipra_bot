from types import NoneType
from typing import Iterable
import asyncio, aiosqlite, sqlite3

class Database:
    def __init__(self, db_name: str, table_name: str) -> None:
        self.db_path = f"databases/{db_name}.db"
        self.table = table_name
        
    async def _init_db(self) -> None:
        """It's better to don't execute it on outside of this class"""
        self.db = await aiosqlite.connect(self.db_path)
        self.cur = await self.db.cursor()

    async def _close_db(self) -> None:
        """It's better to don't execute it on outside of this class"""
        await self.cur.close()
        await self.db.close()

    async def _commit_db(self) -> bool | None:
        """It's better to don't execute it on outside of this class"""
        is_error = True
        while is_error:
            try:
                await self.db.commit()
                is_error = False
                return True
            except sqlite3.OperationalError as e:
                if 'database is locked' in str(e).lower():
                    is_error = True
                elif 'database or disk is full' in str(e).lower():
                    exit("ERROR! DATABASE OR DISK IS FULL!")
                else:
                    raise e

    async def execute(self, cmd: str, params: Iterable = None) -> sqlite3.Cursor:
        await self._init_db()
        result = await self.cur.execute(cmd, params)
        r = await self._commit_db()
        await self._close_db() if r == True else None
        return result

    async def get_data(
        self, selects: list | tuple | set | None = None, 
        wheres: dict | None = None
        ) -> Iterable[sqlite3.Row] | None:
        # Check types
        if not isinstance(selects, (list, tuple, set, NoneType)) or not isinstance(wheres, (dict, NoneType)):
            raise TypeError

        try:
            # Initialize database
            await self._init_db()

            # Generate command
            params = [param for _, param in wheres.items()] if not isinstance(wheres, NoneType) else []
            
            if isinstance(selects, NoneType) and isinstance(wheres, NoneType):
                cmd = f"SELECT * FROM {self.table}"
            else:
                selects = selects if not isinstance(selects, NoneType) else []
                cols = [f"{col_name}=?" for col_name in wheres] if not isinstance(wheres, NoneType) else []
                cmd = "SELECT "
                cmd += ", ".join(selects) if selects != [] else "* "
                cmd += f" FROM {self.table} WHERE " if cols != [] else f" FROM {self.table}"
                cmd += " AND ".join(cols) if cols != [] else ""

            # Execute and fetch result
            await self.cur.execute(cmd, params)
            fetched = await self.cur.fetchall()

            # Safe close database
            await self._close_db()

            # Return result
            return fetched
        except Exception as e:
            await self._close_db()
            raise e

    async def insert_data(self, inserts: dict) -> None:
        # Check types
        if not isinstance(inserts, dict):
            raise TypeError
        try:
            # Initialize database
            await self._init_db()

            # Generate command
            cols = [col for col in inserts]
            params = [param for _, param in inserts.items()]
            cmd = f"INSERT INTO {self.table}("
            cmd += ", ".join(cols)
            cmd += ") VALUES("
            cmd += ", ".join("?" for _ in inserts)
            cmd += ")"

            # Execute time!
            await self.cur.execute(cmd, params)

            # Commit to db
            r = await self._commit_db()

            # Don't forget to close the database
            if r == True:
                await self._close_db()

            return None
        except Exception as e:
            await self._close_db()
            raise e

    async def update_data(self, new: dict, conditions: dict) -> None:
        # Check types
        if not isinstance(new, dict) or not isinstance(conditions, dict):
            raise TypeError

        try:
            # Some needed variable
            params = [n for _, n in new.items()] + [c for _, c in conditions.items()]
            cols = [f"{col}=?" for col in new]
            cons = [f"{con}=?" for con in conditions]

            # Generate command
            cmd = f"UPDATE {self.table} SET " 
            cmd += ", ".join(cols) 
            cmd += " WHERE " 
            cmd += " AND ".join(cons)
            cmd = cmd.strip()

            # Init db
            await self._init_db()

            # Execute command
            await self.cur.execute(cmd, params)

            # Commit to databse
            r = await self._commit_db()

            # Safely close database
            if r == True:
                await self._close_db()

            return None
        except Exception as e:
            await self._close_db()
            raise e

    async def delete_data(self, wheres: dict) -> None:
        # Check types
        if not isinstance(wheres, dict):
            raise TypeError

        try:
            # Needed variables
            cols = [f"{col}=?" for col in wheres]
            params = [p for _, p in wheres.items()]

            # Generate sql command
            cmd = f"DELETE FROM {self.table} WHERE "
            cmd += ", ".join(cols)
            cmd = cmd.strip()

            # Init db
            await self._init_db()

            # Execute cmd
            await self.cur.execute(cmd, params)

            # Commit to db
            r = await self._commit_db()

            # Safely close the db
            if r == True:
                await self._close_db()

            return None
        except Exception as e:
            await self._close_db()
            raise e

if __name__ == '__main__':
    # Tests
    async def test():
        db = Database('test', 'my_table')
        await db.insert_data({'name': 'Aziz Ridhwan Pratama', 'age': 15, 'country': 'Indonesia'})
        print(await db.get_data(wheres = {'country': 'Indonesia'}))
        db = Database('test', 'my_table')
        await db.update_data({'age': 16}, {'id': 4})
        print(await db.get_data({'name', 'age'}, {'country': 'Malaysia'}))
        db = Database('test', 'my_table')
        await db.delete_data({'id': 4})
        print(await db.get_data({'name', 'age'}))

    asyncio.run(test())