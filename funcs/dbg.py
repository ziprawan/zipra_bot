import aiofiles, os
from utils.helper import get_length
from telethon.tl.custom.message import Message
from telethon.tl.types import MessageEntityCode
from telethon.extensions.markdown import add_surrogate, del_surrogate

async def main(*args):
    event: Message = args[0]
    
    if (await event.get_reply_message()) != None:
        msg = (await event.get_reply_message()).stringify()
    else:
        msg = event.stringify()

    length = get_length(msg)
    if length > 4096:
        async with aiofiles.open("debug.txt", "w") as file:
            await file.write(msg)
            await file.close()
        await event.client.send_file(
            event.chat_id,
            'debug.txt'
        )
        if os.path.exists('debug.txt'):
            os.remove('debug.txt')
        return True
    else:
        return await event.reply(
            msg,
            formatting_entities = [MessageEntityCode(
                offset = 0,
                length = length
            )]
        )