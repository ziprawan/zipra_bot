class CallbackParser:
    def __init__(self, text: str|bytes):
        if isinstance(text, bytes):
            text = text.decode()
        if not isinstance(text, str):
            raise TypeError(f"We need 'str' type. Not {type(text)}!")
        # Ex. pin_1234567890_loud
        self.splitted = text.split('_', 2) # ['pin', '1234567890', 'loud']
    
    async def get_command(self):
        return self.splitted[0]
    
    async def get_user(self):
        return self.splitted[1]
    
    async def get_options(self):
        return self.splitted[2]

class Parser:
    def __init__(self, username: str, text: str):
        self.uname = username.lower()
        self.text = text
        self.prefix = ['/', '!', '$', '\\']
    
    async def get_command(self, return_bot_command: bool = False):
        text: str = self.text # Example: /start@test_bot args
        if text == None:
            return None
        username = self.uname
        prefix = self.prefix
        if text[0] in prefix:
            if '\n' in text:
                splitted = text.splitlines()
                if ' ' in splitted[0]:
                    splitted = splitted[0].split()
            else:
                splitted = text.split()
            
            command = splitted[0]
            splitted_with_prefix = command.split(command[0])
            if '@' in command:
                cmd_splitted = splitted_with_prefix[1].split('@')
                if cmd_splitted[1].lower() == username.lower():
                    if return_bot_command:
                        return command
                    else:
                        actual_cmd = cmd_splitted[0]
                        return actual_cmd.lower()
                else:
                    return None
            else:
                if return_bot_command:
                    return command
                else:
                    return splitted_with_prefix[1]
        else:
            return None

    async def get_args(self):
        text = self.text
        command = await self.get_command(True)
        if text == None or command == None:
            return None
        else:
            replaced = text.replace(command, '')
            stripped = replaced.strip()
            if stripped == '':
                return None
            else:
                return stripped
# Tests
if __name__ == '__main__':
    import asyncio
    text_to_test = [
        "/start",
        "/start@Ziprathon_bot",
        "/StArt@ZiPrAthON_BoT",
        "/start@other_bot",
        "/start Hello ngabs",
        "/start@Ziprathon_bot This is args",
        "/StArt@ZiPrAthON_BoT args too",
        "/start\nArgs in newline",
        "/start@Ziprathon_bot\nYahahahah",
        "/StArt@ZiPrAthON_BoT\nWahyu wahyu"
    ]
    uname = "Ziprathon_bot"
    for text in text_to_test:
        # print("==========")
        parser = Parser(uname, text)
        cmd = asyncio.run(parser.get_command())
        args = asyncio.run(parser.get_args())
        print(f"Text: {text}\nCommand: {cmd}\nArgs: {args}")
        print("==========")