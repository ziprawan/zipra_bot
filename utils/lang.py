from telethon.tl.custom.message import Message
from utils.database import Database
from utils.init import supported_lang
import xml.etree.ElementTree as ElementTree, os, logging

msg_lang_root = {}
misc_lang_root = {}

for lang in supported_lang:
    misc_file = f'utils/langs/{lang}/misc.xml'
    msg_file = f'utils/langs/{lang}/messages.xml'

    if not os.path.exists(misc_file) or not os.path.exists(msg_file):
        logging.error(f'[LangHandler] Missing language files for {lang}')
        raise FileNotFoundError('Language data missing!')

    misc_root = ElementTree.parse(misc_file).getroot()
    msg_root = ElementTree.parse(msg_file).getroot()
    msg_lang_root[lang] = msg_root
    misc_lang_root[lang] = misc_root

class Language:
    def __init__(self, msg: Message):
        # Declare variables
        db = Database('groups', 'lang')

        self.db = db
        self.msg = msg

    async def get(self, string_name: str, is_misc: bool = False) -> str or None:
        # Check types
        if not isinstance(string_name, str) or not isinstance(is_misc, bool):
            raise TypeError

        db = self.db
        msg = self.msg

        if (await db.check_table('lang')) == False:
            await db.execute("CREATE TABLE IF NOT EXISTS lang (id integer PRIMARY KEY, chat_id integer NOT NULL, lang_code text(5))")

        chat_id = msg.chat_id
        fetched = await db.get_data(['lang_code'])
        # fetched = await db.get_data("SELECT lang_code FROM lang WHERE chat_id = %d" % chat_id)
        if fetched == []:
            lang_code = 'en'
        else:
            lang = fetched[0]['lang_code']
            if lang in supported_lang:
                lang_code = lang
            else:
                lang_code = 'en'

        # Read lang file
        if is_misc:
            root = misc_lang_root[lang_code]
        else:
            root = msg_lang_root[lang_code]

        lang_data = {}
        for i in root:
            if i.tag == 'string':
                lang_data[i.attrib['name']] = i.text
        if string_name in lang_data:
            return lang_data[string_name].replace(r"\n", "\n")
        else:
            return "null"
