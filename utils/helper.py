# ---------- Import needed libs ----------
import sqlite3
import struct
from telethon.tl.custom.message import Message
from telethon import functions, types

# ---------- Classes ----------
class Database:
    def __init__(self, database):
        db_path = f'databases/{database}'
        self.db = sqlite3.connect(db_path)
        self.cur = self.db.cursor()
        self.exec = self.cur.execute
        self.commit = self.db.commit

# ---------- Async functions ----------

async def check_admin(event: Message):
    """My helper to detect he's admin or not.
    If in private, just return True, because no admin in private chat"""
    if event.is_private:
        return True

    chat = await event.get_chat()
    sender = (await event.get_sender())
    try:
        result: types.channels.ChannelParticipant = await event.client(functions.channels.GetParticipantRequest(
            channel = chat,
            participant = sender
        ))
        
        if isinstance(result.participant, (types.ChannelParticipantAdmin, types.ChannelParticipantCreator)):
            return True
        else:
            return False
    except Exception as e:
        return await event.respond(f"Error while retreiving admin info.\n\n{str(e)}")

# ---------- End async functions ----------
# ---------- Sync functions ----------

def add_surrogate(text):
    """Adding surrogate to the text.
    SMP -> Surrogate Pairs (Telegram offsets are calculated with these).
    See https://en.wikipedia.org/wiki/Plane_(Unicode)#Overview for more.
    
    Big thanks to telethon dev!"""
    return "".join(
        "".join(
            chr(y) for y in struct.unpack("<HH", x.encode("utf-16le"))
        ) if (0x10000 <= ord(x) <= 0x10FFFF)
        else x
        for x in text
    )

def get_length(text):
    """Count Length of text with surrogate addition"""
    return len(add_surrogate(text))

def ol_generator(text: str, var: list, res: list):
    """My helper for offset and length generator for formatting_entities"""
    offsets = []
    lengths = []
    if isinstance(var, list) and isinstance(res, list):
        if len(var) != len(res):
            return None
        
        for i in range(len(var)):
            var[i] = '{' + var[i] + '}'

        for i in res:
            lengths.append(get_length(str(i)))
        
        for j in range(len(lengths)):
            tmp = text.find(var[j])
            if j != 0:
                add, subtract = 0, 0
                for k in range(j):
                    add += get_length(str(res[k]))
                    subtract += len(var[k])
                tmp += add - subtract
            offsets.append(tmp)
        
        return offsets, lengths
    else:
        return None

# ---------- End sync functions ----------