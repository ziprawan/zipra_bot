from telethon.tl.custom.message import Message
import xml.etree.ElementTree as ElementTree
import os, asyncio

supported_lang = ['id', 'en', 'ar', 'ja', 'ms']

class Language:
    def __init__(self, msg: Message):
        # Declare variables
        self.msg = msg
    
    async def get(self, string_name: str, is_button: bool = False) -> str or None:
        # Check types
        if not isinstance(string_name, str) or not isinstance(is_button, bool):
            raise TypeError

        msg = self.msg

        lang = (await msg.get_sender()).lang_code

        # Read lang file
        file = f'utils/langs/{lang}/string.xml'
        if not os.path.exists(file):
            raise FileNotFoundError("Language file not found!")
        
        parsed = ElementTree.parse(file)
        
        root = parsed.getroot()

        if is_button:
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
            return None