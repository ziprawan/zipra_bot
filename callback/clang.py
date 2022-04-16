import logging
from telethon.events.callbackquery import CallbackQuery
from telethon.tl.types import MessageEntityCode
from utils.helper import check_perm, ol_generator
from utils.database import Database
from utils.lang import Language, supported_lang
from utils.parser import CallbackParser

async def main(*args):
    logging.debug("[LangCallback] Called. Setting up variables")
    event: CallbackQuery.Event = args[0]
    parser: CallbackParser = args[1]
    lang = Language(event)
    db = Database('groups', 'lang')

    # In case if database is missing
    if (await db.check_table('lang')) == False:
        await db.execute("CREATE TABLE IF NOT EXISTS lang (id integer PRIMARY KEY, chat_id integer NOT NULL, lang_code text(5))")

    if not event.is_private:
        can_change_info = await check_perm(event, 'change_info')
        if not can_change_info:
            logging.debug("[LangCallback] User doesn't have change_info permission")
            return await event.answer(
                message = (await lang.get('missing_perms', True)).format(perm='change_info'),
                alert = True
            )

    logging.debug("[LangCallback] User is admin")
    logging.debug("[LangCallback] Parsing options")
    chat_id = event.chat_id
    lang_code = parser.args
    logging.debug("[LangCallback] Fetching data from database")
    fetched = await db.get_data({'lang_code'}, {'chat_id': chat_id})

    if lang_code not in supported_lang:
        logging.error("[LangCallback] Language code not supported")
        return await event.edit("Internal error")
    
    if fetched == []:
        logging.info("[LangCallback] Data empty. Inserting new data")
        await db.insert_data({'chat_id': chat_id, 'lang_code': lang_code})
    else:
        logging.info("[LangCallback] Data found. Updating data")
        await db.update_data({'lang_code': lang_code}, {'chat_id': chat_id})

    logging.debug(f"[LangCallback] Successfully set language to {lang_code}")
    logging.debug("[LangCallback] Generating message and entities")
    successful_msg = await lang.get('change_lang_success')
    offs, lens = ol_generator(successful_msg, ['lang_name'], [supported_lang[lang_code]])
    
    logging.debug("[LangCallback] Editing message")
    return await event.edit(
        successful_msg.format(
            lang_name = supported_lang[lang_code]
        ),
        formatting_entities = [
            MessageEntityCode(
                offset = offs[0],
                length = lens[0]
            )
        ]
    )

