from utils.lang import Language
from telethon.tl.custom.message import Message
from telethon.tl.types import InputMessageEntityMentionName, InputUser

async def main(*args):
    event: Message = args[0]
    params = await args[1].get_options()
    lang = Language(event)
    sender = await event.get_sender()

    if not event.is_private:
        return await event.reply(
            (await lang)
        )