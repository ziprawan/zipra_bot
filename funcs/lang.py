from utils.helper import Database, check_admin, ol_generator
from utils.init import supported_lang
from utils.lang import Language
from telethon.tl.types import (
    KeyboardButtonRow,
    KeyboardButtonCallback,
    MessageEntityCode,
    ReplyInlineMarkup
)

async def main(*args):
    event = args[0]
    lang = Language(event)
    sender = await event.get_sender()

    if not (await check_admin(event)):
        return await event.reply(await lang.get('admin_error'))

    chat_id = event.chat_id
    db = Database('groups.db')

    db.exec("""
    CREATE TABLE IF NOT EXISTS lang (
        id integer PRIMARY KEY,
        chat_id integer NOT NULL,
        lang_code text(5)
    )
    """)
    
    db.exec("SELECT lang_code FROM lang WHERE chat_id = ?", (chat_id,))

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
    
    if buttons != []:
        rows.append(KeyboardButtonRow(buttons))

    fetched = db.cur.fetchall()
    if fetched == []:
        await event.reply(
            "Current lang is en\nSelect language:",
            buttons = ReplyInlineMarkup(rows)
        )
    else:
        msg = "Current lang is: {lang_name}\nSelect language:"
        detected_lang = fetched[0][0]
        if detected_lang not in supported_lang:
            lang_name = "not supported"
        else:
            lang_name = supported_lang[detected_lang]

        offs, lens = ol_generator(msg, ['lang_name'], [lang_name])
        print(offs, lens)
        entities = MessageEntityCode(offs[0], lens[0])
        
        await event.reply(
            msg.format(lang_name = lang_name),
            buttons = ReplyInlineMarkup(rows),
            formatting_entities = [entities]
        )