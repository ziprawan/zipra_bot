import asyncio, time
from telethon.tl.custom.message import Message
from utils.init import owner
from telethon import errors
from utils.lang import Language
from io import BytesIO

async def errors_handler(error, event: Message, traceback):
    lang = Language(event)
    if isinstance(error, errors.FloodWaitError):
        return await asyncio.sleep(error.seconds)
    elif isinstance(error, errors.ChatAdminRequiredError):
        return await event.reply((await lang.get("me_not_admin")))
    elif isinstance(error, errors.MessageTooLongError):
        msg = error.request.message
        with BytesIO(str.encode(msg)) as out:
            out.name = f"{error.__class__.__name__}_{round(time.time())}.txt"
            return await event.respond(file=out)
    else:
        await event.respond(f"Something went wrong\n\n`{str(error)}`\n\nPlease report it to @Pra210906")
        with BytesIO(str.encode(str(traceback))) as out:
            out.name = f"{error.__class__.__name__}_{round(time.time())}.txt"
            return await event.client.send_message(owner, error.args[0], file=out)