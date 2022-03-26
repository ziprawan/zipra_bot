import asyncio, time, logging
from io import BytesIO
from telethon import errors
from telethon.tl.custom.message import Message
from telethon.tl.types import (
    KeyboardButtonRow,
    KeyboardButtonUserProfile,
    InputKeyboardButtonUserProfile,
    MessageEntityCode,
    ReplyInlineMarkup,
)
from utils.helper import ol_generator
from utils.init import owner
from utils.lang import Language

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
        input_owner = await event.client.get_input_entity(owner)
        msg = await lang.get('unhandled_error')
        var = ['error']
        res = [str(error)]
        offs, lens = ol_generator(msg, var, res)
        entities = [MessageEntityCode(offs[0], lens[0])]
        msg = msg.format(error = str(error))
        await event.respond(
            msg,
            formatting_entities = entities,
            buttons = ReplyInlineMarkup([
                KeyboardButtonRow([
                    InputKeyboardButtonUserProfile(
                        text = await lang.get('contact_us', True),
                        user_id = input_owner
                    )
                ])
            ])
        )
        with BytesIO(str.encode(str(traceback))) as out:
            out.name = f"{error.__class__.__name__}_{round(time.time())}.txt"
            return await event.client.send_message(owner, error.args[0], file=out)