import logging, time
from datetime import datetime
from utils.lang import Language
from telethon.tl.types import MessageEntityCode
from telethon.tl.custom.message import Message

async def main(*args):
    logging.debug("[PingHandler] Sending message")
    event: Message = args[0]
    lang = Language(event)
    resp_text = "🏓 PONG!"

    logging.debug("[PingHandler] Getting response time")
    now = time.time()
    msg_time = datetime.timestamp(event.date)
    resp_time = round((now - msg_time) * 1000, 3)
    logging.debug("[PingHandler] Ping time is " + str(resp_time))

    logging.debug("[PingHandler] Appending message")
    resp_text += "\n" + await lang.get('response_time')
    offset = len(resp_text) + 1
    resp_text += str(resp_time) + " ms"
    length = len(str(resp_time) + " ms")

    logging.debug("[PingHandler] Sending message with response time")
    return await event.reply(
        resp_text,
        formatting_entities = [MessageEntityCode(
            offset = offset,
            length = length
        )]
    )