import asyncio
from telethon.tl.custom.message import Message
from telethon.tl.types import MessageEntityTextUrl
from utils.init import owner
from telethon import errors
from utils.lang import Language

async def errors_handler(error, event: Message, traceback):
    lang = Language(event)
    if isinstance(error, errors.FloodWaitError):
        return await asyncio.sleep(error.seconds)
    elif isinstance(error, errors.ChatAdminRequiredError):
        return await event.reply((await lang.get("me_not_admin")))
    else:
        await event.respond(f"Something went wrong\n\n`{str(error)}`\n\nPlease report it to @Pra210906")
        return await event.client.send_message(owner, str(traceback))

    