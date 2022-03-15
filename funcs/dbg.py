import aiofiles, os, logging, time
from utils.helper import get_length
from telethon.tl.custom.message import Message
from telethon.tl.types import MessageEntityCode

async def main(*args):
    event: Message = args[0]
    logging.debug("[DebugHandler] Assigning message text")
    if (await event.get_reply_message()) != None:
        logging.info("[DebugHandler] Reply message detected. Using replied message object instead")
        msg = (await event.get_reply_message()).stringify()
    else:
        logging.info("[DebugHandler] No reply message detected. Using self message object instead")
        msg = event.stringify()

    logging.debug("[DebugHandler] Getting length")
    length = get_length(msg)
    logging.debug("[DebugHandler] Check length of message using variable 'length'")
    if length > 4096:
        logging.info("[DebugHandler] Length exceeds 4096. Sending as file instead")
        logging.info("[DebugHandler] Writing message to file")
        filename = f"debug_{round(time.time())}.txt"
        async with aiofiles.open(filename, "w") as file:
            await file.write(msg)
            logging.debug(f"[DebugHandler] Saving file as {filename}")
            await file.close()
        logging.info("[DebugHandler] Sending file")
        await event.client.send_file(
            event.chat_id,
            filename
        )
        logging.debug("[DebugHandler] Removing temp file")
        if os.path.exists(filename):
            os.remove(filename)
        return True
    else:
        logging.info("[DebugHandler] Length doesn't exceed 4096")
        logging.debug("[DebugHandler] Sending message")
        return await event.reply(
            msg,
            formatting_entities = [MessageEntityCode(
                offset = 0,
                length = length
            )]
        )