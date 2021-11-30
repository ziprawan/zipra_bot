import sqlite3
from typing import Iterable

db = sqlite3.connect("utils/data.db", check_same_thread=False)
cur = db.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS service(id int, option text(5))")

async def get_data(group):
    command = "SELECT * FROM service where id=?"
    cur.execute(command, (group,))
    fetched = cur.fetchall()
    try:
        result = fetched[0][1]
    except:
        return None
    if result == "false":
        return False
    elif result == "true":
        return True
    else:
        raise ValueError("Invalid Result!")

async def insert_data(group, option):
    if option == True:
        op = "true"
    elif option == False:
        op = "false"
    else:
        raise ValueError("Invalid Option!")
    
    hmm = await get_data(group)
    if hmm == None:
        if op == "true":
            cur.execute("INSERT INTO service(id, option) VALUES(?, ?)", (group, op,))
            db.commit()
            return True
        elif op == "false":
            cur.execute("INSERT INTO service(id, option) VALUES(?, ?)", (group, op,))
            db.commit()
            return False
        else:
            raise ValueError("Oh")
    elif hmm == True:
        if op == "true":
            return True
        elif op == "false":
            cur.execute("UPDATE service SET option=? WHERE id=?", (op, group,))
            db.commit()
            return False
        else:
            raise ValueError("Oh")
    elif hmm == False:
        if op == "false":
            return False
        elif op == "true":
            cur.execute("UPDATE service SET option=? WHERE id=?", (op, group,))
            db.commit()
            return True
        else:
            raise ValueError("Oh (2)")
    else:
        raise ValueError("Hmmmmmmmm")