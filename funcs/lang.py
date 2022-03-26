import logging
from utils.database import MyDatabase
from utils.helper import check_perm, ol_generator
from utils.init import supported_lang
from utils.lang import Language
from telethon.tl.patched import Message, User
from telethon.tl.types import (
    KeyboardButtonRow,
    KeyboardButtonCallback,
    MessageEntityCode,
    ReplyInlineMarkup
)

async def main(*args):
    logging.debug("[LangHandler] Setting up variables")
    event: Message = args[0]
    lang = Language(event)
    sender: User = await event.get_sender()

    if not event.is_private and not (await check_perm(event, 'change_info')):
        logging.info("[LangHandler] User doesn't have change_info permission. Aborting")
        msg = await lang.get('missing_perms')
        var = ['perm']
        res = ['change_info']
        offs, lens = ol_generator(msg, var, res)
        entities = [MessageEntityCode(offset = offs[0], length = lens[0])]
        return await event.reply(msg.format(perm=res[0]), formatting_entities = entities)

    logging.debug("[LangHandler] Creating buttons")
    rows = []
    buttons = []

    for i in supported_lang:
        lang_code = i
        lang_name = supported_lang[i]
        if len(buttons) == 2:
            rows.append(KeyboardButtonRow(buttons))
            buttons = []
        
        buttons.append(KeyboardButtonCallback(
            text = lang_name,
            data = f"setlang_{sender.id}_{lang_code}".encode()
        ))

    logging.debug("[LangHandler] Getting data from database")
    chat_id = event.chat_id
    db = MyDatabase('groups.db')

    await db.exec("CREATE TABLE IF NOT EXISTS lang (id integer PRIMARY KEY, chat_id integer NOT NULL, lang_code text(5))")
    
    fetched = await db.get_data("SELECT lang_code FROM lang WHERE chat_id = %d" % chat_id)
    
    if buttons != []:
        rows.append(KeyboardButtonRow(buttons))

    if fetched == []:
        logging.debug(f"[LangHandler] No lang data found for chat {chat_id}")
        lang_name = supported_lang['en']
    else:
        detected_lang = fetched[0]['lang_code']
        logging.debug(f"[LangHandler] Found lang data for chat {chat_id}: [{detected_lang}]")

        if detected_lang not in supported_lang:
            logging.warn(f"[LangHandler] Lang \"{detected_lang}\" is not found or not supported! Displaying as not supported")
            lang_name = "not supported"
        else:
            logging.debug("[LangHandler] Lang supported")
            lang_name = supported_lang[detected_lang]

    logging.debug("[LangHandler] Generating message and formatting_entities")
    msg = "Current lang is: {lang_name}\nSelect language:"

    offs, lens = ol_generator(msg, ['lang_name'], [lang_name])
    entities = MessageEntityCode(offs[0], lens[0])

    logging.debug("[LangHandler] Send Message")
    await event.reply(
        msg.format(lang_name = lang_name),
        buttons = ReplyInlineMarkup(rows),
        formatting_entities = [entities]
    )
