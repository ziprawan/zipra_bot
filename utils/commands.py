class Parser:
    def __init__(self, username, text):
        self.uname = username
        self.text = text
        self.prefix = ['/', '!', '$']
    async def get_options(self, tujuan):
        pesan = self.text
        if pesan == None:
            return None
        uname = self.uname
        split_space = pesan.split(" ")
        if len(split_space) <= 1:
            return None
        else:
            for i in self.prefix:
                if i == pesan[0]:
                    perintah = split_space[0].split(i)
                    if type(tujuan) == list:
                        for j in tujuan:
                            tujuan_by_uname = f'{j}@{uname}'
                            if perintah[1] == j or perintah[1] == tujuan_by_uname:
                                hmm = pesan.replace(split_space[0], '', 1)
                                args = hmm.replace(' ', '', 1)
                                return args
                        return None
                    elif type(tujuan) == str:
                        tujuan_by_uname = f'{tujuan}@{uname}'
                        if perintah[1] == tujuan or perintah[1] == tujuan_by_uname:
                            hmm = pesan.replace(split_space[0], '', 1)
                            args = hmm.replace(' ', '', 1)
                            return args
                        else:
                            return None
                    else:
                        return None
    
    async def get_command(self):
        teks = self.text # Misalkan /json@zipra_bot tes
        if teks == None:
            return None
        uname = self.uname # zipra_bot
        prefix = self.prefix # Ada $ / dan !
        split_by_space = teks.split(' ') # /json@ziprabot dan tes
        if teks[0] in prefix:
            split_by_prefix = split_by_space[0].split(teks[0]) # '' dan json@zipra_bot
            split_by_tag = split_by_prefix[1].split('@') # json dan zipra_bot
            if len(split_by_tag) == 1:
                return split_by_tag[0]
            if split_by_tag[1] == uname or split_by_tag[1] == '':
                return split_by_tag[0] # Return 'json'


# Just for testing purposes
if __name__ == '__main__':
    parse = Parser('zipra_bot', '/json@zipra_bot /json@ziprabot lah kok wkwkwk')
    print(parse.extract_command('json'))
    print(parse.get_command())
