from pyrogram import types
from utils.databases import Database
import time

async def is_restricted(msg: types.Message):
    db = Database("databases/cooldown.db", "cooldown_data")
    db.execute("CREATE TABLE IF NOT EXISTS cooldown_data(id AUTO_INCREMENT PRIMARY KEY, user_id INT NOT NULL, until INT DEFAULT 0, many INT DEFAULT 0)")

    now = round(time.time())

    # Defining user id. This variable can be user id or chat id
    user_id = msg.from_user.id if msg.from_user else msg.sender_chat.id

    fetched = db.get_data(['user_id'], [user_id])
    
    if fetched != []:
        many = fetched[0][3]
        if many + 1 > 5:
            db.update_data()
            return True
        else:
            pass
    else:
        return False # Return False because user currently not in database