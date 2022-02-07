from time import time
from datetime import datetime
from utils.lang import Language
from telethon.tl.types import MessageEntityCode
from telethon.tl.custom.message import Message

async def main(*args):
    event: Message = args[0]
    lang = Language(event)

    resp_text = "🏓 PONG!"
    answer = await event.reply(resp_text)

    now = time()
    msg_time = datetime.timestamp(answer.date)
    resp_time = round((now - msg_time) * 1000, 3)
    
    resp_text += "\n" + await lang.get('response_time')
    offset = len(resp_text) + 1
    resp_text += str(resp_time) + " ms"
    length = len(str(resp_time) + " ms")

    return await answer.edit(
        resp_text,
        formatting_entities = [MessageEntityCode(
            offset = offset,
            length = length
        )]
    )