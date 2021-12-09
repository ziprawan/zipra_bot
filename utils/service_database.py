from utils.databases import Database
import asyncio

db = Database("databases/data.db", 'service')
asyncio.run(db.execute("CREATE TABLE IF NOT EXISTS service(id int, option text(5))"))

async def get_data(group):
    fetched = await db.get_data(['id'], [group])
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
            await db.insert_data(['id', 'option'], [group, op])
            return True
        elif op == "false":
            await db.insert_data(['id', 'option'], [group, op])
            return False
        else:
            raise ValueError("Oh")
    elif hmm == True:
        if op == "true":
            return True
        elif op == "false":
            await db.update_data(['option'], [op], ['id'], [group])
            return False
        else:
            raise ValueError("Oh")
    elif hmm == False:
        if op == "false":
            return False
        elif op == "true":
            await db.update_data(['option'], [op], ['id'], [group])
            return True
        else:
            raise ValueError("Oh (2)")
    else:
        raise ValueError("Hmmmmmmmm")