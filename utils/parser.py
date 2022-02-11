class CallbackParser:
    def __init__(self, text: str):
        if not isinstance(text, str):
            raise TypeError(f"We need 'str' type. Not {type(text)}!")
        # Ex. pin_1234567890_loud
        self.splitted = text.split('_', 2) # ['pin', '1234567890', 'loud']
    
    def get_command(self):
        return self.splitted[0]
    
    def get_user(self):
        return self.splitted[1]
    
    def get_options(self):
        return self.splitted[2]

class Parser:
    def __init__(self, username: str, text: str):
        self.uname = username.lower()
        self.text = text
        self.prefix = ['/', '!', '$', '\\']
    
    async def get_command(self, lower:bool=True):
        teks: str = self.text # Example /start@examplebot
        if teks == None:
            return None
        uname = self.uname # examplebot
        prefix = self.prefix # Ada $ / dan ! dll
        if teks[0] in prefix:
            if '\n' in teks:
                splitted = teks.split("\n", 1)
                if ' ' in splitted[0]:
                    splitted = teks.split(' ', 1)
            else:
                splitted = teks.split(' ', 1)
            split_by_space = splitted
            split_by_prefix = split_by_space[0].split(teks[0]) # '' dan json@zipra_bot
            split_by_tag = split_by_prefix[1].split('@') # json dan zipra_bot
            if len(split_by_tag) == 1:
                if not lower:
                    return split_by_tag[0]
                return split_by_tag[0].lower()
            if split_by_tag[1].lower() == uname or split_by_tag[1] == '':
                if not lower:
                    return split_by_tag[0]
                return split_by_tag[0].lower() # Return 'json'

    async def get_options(self):
        tujuan = await self.get_command(False)
        pesan = self.text
        if pesan == None or tujuan == None:
            return None
        uname = self.uname
        tmp = pesan.replace(pesan[0]+tujuan, '', 1)
        split_space = pesan.split('\n') if tmp[:1] == '\n' else pesan.split(' ')
        if len(split_space) <= 1:
            return None
        else:
            for i in self.prefix:
                if i == pesan[0]:
                    perintah = split_space[0].split(i)
                    if type(tujuan) == str:
                        tujuan_by_uname = f'{tujuan}@{uname}'
                        if perintah[1] == tujuan or perintah[1] == tujuan_by_uname:
                            hmm = pesan.replace(split_space[0], '', 1)
                            args = hmm.replace('\n', '', 1) if hmm[:1] == '\n' else hmm.replace(' ', '', 1)
                            return args
                        else:
                            return None
                    else:
                        return None