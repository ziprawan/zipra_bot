# Logger

import logging

logging.basicConfig(format="%(asctime)s - %(message)s", level=10)
logging.info("Importing modules...")

import telethon, traceback

if telethon.__version__ != '1.25.1':
    raise ValueError("We need telethon 1.25.1 :)")

from utils.init import *
from utils.commands import commands
from utils.parser import Parser
from utils.errors import errors_handler
from telethon.sync import events
from telethon.tl.custom.message import Message
from telethon.events.callbackquery import CallbackQuery

# Message handler

@client.on(events.CallbackQuery)
async def callback_query_handler(event: CallbackQuery.Event):
    try:
        test = await event.get_sender()
        print(test.id)
        logging.info("Writing file...")
        with open("test.txt", 'w') as file:
            file.write(event.stringify())
            file.close()
        logging.info("Done")
        return await event.answer(
            message = event.query.data.decode(),
            alert = True
        )
    except Exception as e:
        return await errors_handler(e, event)

@client.on(events.NewMessage(incoming=True))
async def message_handler(event: Message):
    try:
        text = event.raw_text if event.raw_text else None
        print(text)

        parser = Parser(me.username, text)
        command = await parser.get_command()

        if command in commands:
            return await commands[command](
                event, parser, me, owner
            )
        else:
            return False
    except Exception as e:
        return await errors_handler(e, event, traceback.format_exc())

logging.info("Program Executed!")
with client:
    client.run_until_disconnected()