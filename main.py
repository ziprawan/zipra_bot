import logging

import telethon
import traceback
from telethon.events.callbackquery import CallbackQuery
from telethon.sync import events
from telethon.tl.custom.message import Message

from utils.chat_action import chat_action
from utils.commands import commands, callbacks, cooldown
from utils.errors import errors_handler
from utils.init import *
from utils.parser import CallbackParser, Parser

if telethon.__version__ != '1.25.1':
    raise ValueError("Install telethon from requirements.txt")

if debug:
    logging.getLogger().setLevel(logging.DEBUG)
else:
    logging.getLogger().setLevel(logging.WARNING)

logging.debug("[Main] Registering event handler")


# Chat Action handler. Like user join/left, chat title changed, etc. (Service Message)
@client.on(events.ChatAction)
async def chat_action_handler(event: events.ChatAction.Event):
    return await chat_action(event)


# Message handler

@client.on(events.CallbackQuery)
async def callback_query_handler(event: CallbackQuery.Event):
    try:
        # My callback data format is:
        #
        # command_userid_arguments
        sender_id = (await event.get_sender()).id
        logging.debug(f"[Callback] Incoming calback data: {event.data.decode()}")
        logging.debug("[Callback] Parsing callback data")
        parser = CallbackParser(event.data)
        logging.debug("[Callback] Getting command of callback")
        cmd = parser.command
        user = parser.user_id
        if int(user) != int(sender_id):
            logging.warning(f"[Callback] user_id at button data ({user}) is different with user clicker ({sender_id})")
        logging.debug("[Callback] Checking the existence of the callback command")
        if cmd in callbacks:
            logging.info(f"[Callback] Command found! Calling callback.{cmd}.main")
            return await callbacks[cmd].main(
                event, parser, me, owner
            )
        else:
            logging.info("[Callback] Command not found")
            return False
    except Exception as e:
        logging.warning("[Callback] Something went wrong. Calling errors_handler")
        return await errors_handler(e, event, traceback.format_exc())


@client.on(events.NewMessage(incoming=True))
async def message_handler(event: Message):
    try:
        in_cooldown = await cooldown(event)
        if in_cooldown:
            logging.info("[NewMessage] User in cooldown.")
            return False
        logging.debug("[NewMessage] Getting text of message")
        text = event.raw_text if event.raw_text else None
        logging.debug(f"[NewMessage] Incoming message: {text}")
        logging.debug("[NewMessage] Parsing text")
        parser = Parser(me.username, text)
        logging.debug("[NewMessage] Getting command")
        command = parser.get_command()
        logging.debug("[NewMessage] Checking the existence of the command")
        logging.debug(f"[NewMessage] Detected command: {command}")
        if command in commands:
            logging.info(f"[NewMessage] Command found! Calling funcs.{command}.main")
            return await commands[command].main(
                event, parser, me, owner
            )
        else:
            logging.info("[NewMessage] Command not found")
            if (await event.get_sender()).id == owner:
                if event.is_private:
                    replied = await event.get_reply_message()
                    if replied is not None:
                        return await commands['report_bug'].answer_report(event, replied)
            return False
    except Exception as e:
        logging.warning("[NewMessage] Something went wrong. Calling errors_handler")
        return await errors_handler(e, event, traceback.format_exc())


logging.debug("[Main] Event handler registered!")
logging.info("[Main] Starting client")
with client:
    client.run_until_disconnected()

logging.info("[Main] Client disconnected")
