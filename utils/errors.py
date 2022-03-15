import asyncio, time, logging
from telethon.tl.custom.message import Message
from utils.init import owner
from telethon import errors
from utils.lang import Language
from io import BytesIO

async def errors_handler(error: Exception, event: Message, traceback):
    logging.warn("[ErrorHandler] Error Type: %s" % error.__class__.__name__)
    logging.warn("[ErrorHandler] Error Message: %s" % error)
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
    elif isinstance(error, errors.MessageNotModifiedError):
        pass
    elif isinstance(error, errors.MessageIdInvalidError):
        pass
    else:
        await event.respond(f"Something went wrong\n\n`{str(error)}`\n\nPlease report it to @Pra210906")
        with BytesIO(str.encode(str(traceback))) as out:
            out.name = f"{error.__class__.__name__}_{round(time.time())}.txt"
            return await event.client.send_message(owner, error.args[0], file=out)