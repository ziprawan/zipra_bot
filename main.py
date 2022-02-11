# Logger

import logging

logging.basicConfig(format="%(asctime)s - %(message)s", level=10)
logging.info("Importing modules...")

import telethon, traceback

if telethon.__version__ != '1.25.1':
    raise ValueError("We need telethon 1.25.1 :)")

from utils.init import *
from utils.commands import commands, callbacks
from utils.parser import CallbackParser, Parser
from utils.errors import errors_handler
from telethon.sync import events
from telethon.tl.custom.message import Message
from telethon.events.callbackquery import CallbackQuery

# Message handler

@client.on(events.CallbackQuery)
async def callback_query_handler(event: CallbackQuery.Event):
    try:
        # My callback data format is:
        #
        # command_userid_arguments

        parser = CallbackParser(event.data)

        cmd = parser.get_command()

        if cmd in callbacks:
            return await callbacks[cmd].main(
                event, parser, me, owner
            )
        else:
            return False
    except Exception as e:
        return await errors_handler(e, event, traceback.format_exc())

@client.on(events.NewMessage(incoming=True))
async def message_handler(event: Message):
    try:
        text = event.raw_text if event.raw_text else None

        parser = Parser(me.username, text)
        command = await parser.get_command()

        if command in commands:
            return await commands[command].main(
                event, parser, me, owner
            )
        else:
            return False
    except Exception as e:
        return await errors_handler(e, event, traceback.format_exc())

logging.info("Program Executed!")
with client:
    client.run_until_disconnected()