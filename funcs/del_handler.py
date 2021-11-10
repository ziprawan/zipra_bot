from logging import NOTSET
from pyrogram.types import Message

def main(msg: Message, *another):
    try:
        if msg.reply_to_message == None:
            return msg.delete()
        else:
            msg.reply_to_message.delete()
            return msg.delete()
    except Exception as e:
        return msg.reply(str(e), True)