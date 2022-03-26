import logging
from utils import init, lang
from telethon.tl.patched import Message

async def main(*args):
    event: Message = args[0]
    sender: int = (await event.get_sender()).id
    my_lang = lang.Language(event)

    if sender == int(init.owner):
        logging.debug("[DebugHandler] Sender is owner")
        if init.debug == True:
            init.debug = False
            logging.getLogger().setLevel(logging.WARN)
            await event.reply(await my_lang.get("debug_off"))
        else:
            init.debug = True
            logging.getLogger().setLevel(level=logging.DEBUG)
            logging.info("[DebugHandler] Debug mode enabled.")
            await event.reply(await my_lang.get('debug_on'))
    else:
        logging.debug("[DebugHandler] Sender is not owner")
    
    return True