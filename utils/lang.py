from telethon.tl.custom.message import Message
from utils.database import MyDatabase
from utils.init import supported_lang
import xml.etree.ElementTree as ElementTree
import os, asyncio

class Language:
    def __init__(self, msg: Message):
        # Declare variables
        db = MyDatabase('groups.db')

        self.db = db
        self.msg = msg

    async def get(self, string_name: str, is_misc: bool = False) -> str or None:
        # Check types
        if not isinstance(string_name, str) or not isinstance(is_misc, bool):
            raise TypeError

        db = self.db
        msg = self.msg

        await db.exec("""
        CREATE TABLE IF NOT EXISTS lang (
            id integer PRIMARY KEY,
            chat_id integer NOT NULL,
            lang_code text(5)
        )
        """)
        chat_id = msg.chat_id
        fetched = await db.get_data("SELECT lang_code FROM lang WHERE chat_id = %d" % chat_id)
        if fetched == []:
            lang_code = 'en'
        else:
            lang = fetched[0]['lang_code']
            if lang in supported_lang:
                lang_code = lang
            else:
                lang_code = 'en'

        lang = lang_code

        # Read lang file
        if is_misc:
            file = f'utils/langs/{lang}/misc.xml'
        else:
            file = f'utils/langs/{lang}/messages.xml'

        if not os.path.exists(file):
            raise FileNotFoundError("Language file not found!")

        parsed = ElementTree.parse(file)
        root = parsed.getroot()

        lang_data = {}
        for i in root:
            if i.tag == 'string':
                lang_data[i.attrib['name']] = i.text
        if string_name in lang_data:
            return lang_data[string_name].replace(r"\n", "\n")
        else:
            return "null"
