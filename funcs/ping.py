import logging
import time
from datetime import datetime

from telethon.tl.custom.message import Message
from telethon.tl.types import MessageEntityCode

from utils.lang import Language
from utils.init import start_time
from utils.helper import convert_seconds


async def main(*args):
    logging.debug("[PingHandler] Sending message")
    event: Message = args[0]
    lang = Language(event)
    resp_text = "🏓 PONG!"

    logging.debug("[PingHandler] Getting response time")
    now = time.time()
    msg_time = datetime.timestamp(event.date)
    resp_time = round((now - msg_time) * 1000, 3)
    now = time.time()
    uptime = round(now - start_time)
    converted = convert_seconds(uptime)
    _str_uptime = "{} days {} hours {} minutes {} seconds.".format(converted[0], converted[1], converted[2], converted[3])
    logging.debug("[PingHandler] Ping time is " + str(resp_time))

    logging.debug("[PingHandler] Appending message")
    resp_text += "\n" + await lang.get('response_time')
    offset = len(resp_text) + 1
    resp_text += str(resp_time) + " ms" + f"\n\nUptime: {_str_uptime}"
    length = len(str(resp_time) + " ms")

    logging.debug("[PingHandler] Sending message with response time")
    return await event.reply(
        resp_text,
        formatting_entities = [MessageEntityCode(
            offset = offset,
            length = length
        )]
    )