class parser:
    def __init__(self, username, text):
        self.uname = username
        self.text = text
        self.prefix = ['/', '!', '$']
    def check_command(self, tujuan, with_option=False):
        try:
            if self.text != None:
                pesan = self.text
                first = pesan[0]
                if first in self.prefix:
                    # Split dengan spasi
                    split_by_space = pesan.split(" ")
                    split_by_tag = split_by_space[0].split('@')
                    command = split_by_tag[0].replace(first, '', 1)
                    args = pesan.replace(split_by_space[0], '')
                    try:
                        if split_by_tag[1] != None and split_by_tag[1] == self.uname:
                            to_my_bot = True
                        else:
                            to_my_bot = False
                    except:
                        to_my_bot = True
                    if to_my_bot == True:
                        if type(tujuan) == list:
                            for i in tujuan:
                                if command == i or command == f'{i}@{self.uname}':
                                    if with_option:
                                        return True
                                    else:
                                        if args == '':
                                            return True
                            return False
                        elif type(tujuan) == str:
                            if command == tujuan or command == f'{tujuan}@{self.uname}':
                                if with_option:
                                    return True
                                else:
                                    if args == '':
                                        return True
                                    else:
                                        return False
                            else:
                                return False
                        else: 
                            return False
                    else:
                        return False
                else:
                    return False
            else:
                return False
        except Exception as e:
            print(str(e))
            return False
    def get_options(self, tujuan):
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
    
    def get_command(self):
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
    parse = parser('zipra_bot', '/json@zipra_bot /json@ziprabot lah kok wkwkwk')
    print(parse.extract_command('json'))
    print(parse.get_command())
