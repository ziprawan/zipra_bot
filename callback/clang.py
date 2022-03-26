import logging
from telethon.events.callbackquery import CallbackQuery
from telethon.tl.types import MessageEntityCode
from utils.helper import check_perm, ol_generator
from utils.database import MyDatabase
from utils.lang import Language, supported_lang

async def main(*args):
    logging.debug("[LangCallback] Called. Setting up variables")
    event: CallbackQuery.Event = args[0]
    parser = args[1]
    can_change_info = await check_perm(event, 'change_info')
    lang = Language(event)
    db = MyDatabase('groups.db')

    if not can_change_info:
        logging.debug("[LangCallback] User doesn't have change_info permission")
        return await event.answer(
            message = (await lang.get('missing_perms', True)).format(perm='change_info'),
            alert = True
        )
    else:
        logging.debug("[LangCallback] User is admin")
        logging.debug("[LangCallback] Parsing options")
        chat_id = event.chat_id
        lang_code = await parser.get_args()
        logging.debug("[LangCallback] Fetching data from database")
        fetched = await db.get_data("SELECT lang_code FROM lang WHERE chat_id = %d" % chat_id)

        if lang_code not in supported_lang:
            logging.error("[LangCallback] Language code not supported")
            return await event.edit("Internal error")
        
        if fetched == []:
            logging.info("[LangCallback] Data empty. Inserting new data")
            await db.exec("INSERT INTO lang (chat_id, lang_code) VALUES (%d, %s)" % (chat_id, MyDatabase.format(lang_code)))
        else:
            logging.info("[LangCallback] Data found. Updating data")
            command = "UPDATE lang SET lang_code = %s WHERE chat_id = %d;" % (MyDatabase.format(lang_code), chat_id)
            await db.exec(command)

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

