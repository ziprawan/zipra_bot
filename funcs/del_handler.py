from logging import NOTSET
from pyrogram.types import Message

async def main(msg: Message, *another):
    try:
        if msg.reply_to_message == None:
            return await msg.delete()
        else:
            await msg.reply_to_message.delete()
            return await msg.delete()
    except Exception as e:
        return await msg.reply(str(e), True)