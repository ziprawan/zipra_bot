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
        chat = await event.get_chat()
        if not event.is_private:
            if chat.username != None:
                link = f"https://t.me/{chat.username}/{event.id}"
            else:
                if chat.megagroup == True:
                    link = f"https://t.me/-100{chat.id}/{event.id}"
                else:
                    link = f"https://t.me/{chat.id}/{event.id}"
        else:
            link = None
        await event.client.send_message(
            owner,
            "Sir, i went wrong while executing this",
            formatting_entities = [MessageEntityTextUrl(
                offset=34,
                length = 4,
                url = link
            )] if link else None,
            link_preview = False
        )
        await event.reply(f"Something went wrong\n\n`{str(error)}`")
        return await event.client.send_message(owner, str(traceback))

    