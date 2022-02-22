from telethon.events.callbackquery import CallbackQuery
from telethon.tl.types import MessageEntityCode
from utils.helper import check_admin, ol_generator
from utils.database import MyDatabase
from utils.lang import Language, supported_lang

async def main(*args):
    event: CallbackQuery.Event = args[0]
    parser = args[1]
    is_admin = await check_admin(event)
    lang = Language(event)
    db = MyDatabase('groups.db')

    if not is_admin:
        return await event.answer(
            message = await lang.get('admin_error', True),
            alert = True
        )
    else:
        chat_id = event.chat_id
        lang_code = await parser.get_options()
        if lang_code not in supported_lang:
            return await event.edit("Internal error")
        successful_msg = await lang.get('change_lang_success')
        offs, lens = ol_generator(successful_msg, ['lang_name'], [supported_lang[lang_code]])
        fetched = await db.get_data("SELECT lang_code FROM lang WHERE chat_id = %d" % chat_id)
        if fetched == []:
            await db.exec("INSERT INTO lang (chat_id, lang_code) VALUES (%d, %s)" % (chat_id, MyDatabase.format(lang_code)))
        else:
            command = "UPDATE lang SET lang_code = %s WHERE chat_id = %d;" % (MyDatabase.format(lang_code), chat_id)
            await db.exec(command)
        
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
