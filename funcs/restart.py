from pyrogram.types import Message
import os

def main(msg: Message, *another):
    owner = 1923158017
    if msg.from_user.id == owner:
        msg.reply("Sesuai permintaan")
        process_id = os.getpid()
        os.system(f"kill -s 15 {process_id} && sleep 3s && bash -c \"python3 bot.py\"")
        # bot.restart()