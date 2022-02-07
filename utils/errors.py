import asyncio
from telethon import errors
from utils.lang import Language

async def errors_handler(error, event):
    lang = Language(event)
    if isinstance(error, errors.FloodWaitError):
        return await asyncio.sleep(error.seconds)
    elif isinstance(error, errors.ChatAdminRequiredError):
        return await event.reply((await lang.get("me_not_admin")))
    else:
        print(error)
    