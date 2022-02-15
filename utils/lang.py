from telethon.tl.custom.message import Message
from utils.helper import Database
from utils.init import supported_lang
import xml.etree.ElementTree as ElementTree
import os, asyncio

class Language:
    def __init__(self, msg: Message):
        # Declare variables
        db = Database('groups.db')

        db.exec("""
        CREATE TABLE IF NOT EXISTS lang (
            id integer PRIMARY KEY,
            chat_id integer NOT NULL,
            lang_code text(5)
        )
        """)
        chat_id = msg.chat_id
        db.exec("SELECT lang_code FROM lang WHERE chat_id = ?", (chat_id,))
        fetched = db.cur.fetchall()
        if fetched == []:
            self.lang_code = 'en'
        else:
            lang = fetched[0][0]
            if lang in supported_lang:
                self.lang_code = lang
            else:
                self.lang_code = 'en'
    
    async def get(self, string_name: str, is_misc: bool = False) -> str or None:
        # Check types
        if not isinstance(string_name, str) or not isinstance(is_misc, bool):
            raise TypeError

        lang = self.lang_code

        # Read lang file
        file = f'utils/langs/{lang}/string.xml'
        if not os.path.exists(file):
            raise FileNotFoundError("Language file not found!")
        
        parsed = ElementTree.parse(file)
        
        root = parsed.getroot()

        if is_misc:
            root = root[1]
        else:
            root = root[0]
        
        lang_data = {}
        for i in root:
            if i.tag == 'string':
                lang_data[i.attrib['name']] = i.text
        
        if string_name in lang_data:
            return lang_data[string_name].replace(r"\n", "\n")
        else:
            return "null"