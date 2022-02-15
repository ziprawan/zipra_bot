from telethon.tl.custom.message import Message

async def main(*args):
    event: Message = args[0]
    parser = args[1]

    # Later my code for bans handlers