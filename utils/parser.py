class Args:
    def __init__(self, splitted_by: str, text: str) -> None:
        self.by = splitted_by
        self.text = text

class CallbackParser:
    def __init__(self, text: str|bytes):
        if isinstance(text, bytes):
            text = text.decode()
        if not isinstance(text, str):
            raise TypeError(f"We need 'str' type, not {type(text)}!")
        # Ex. pin_1234567890_loud
        splitted = text.split('_', 2) # ['pin', '1234567890', 'loud']
        self.command = splitted[0]
        self.user_id = int(splitted[1])
        self.args = splitted[2]

class Parser:
    def __init__(self, username: str, text: str) -> None:
        self.uname = username.lower()
        self.text = text
        self.prefix = ['/', '!', '$', '\\']
    
    def get_command(self, return_bot_command: bool = False) -> str | None:
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
                    return splitted_with_prefix[1].lower()
        else:
            return None

    def get_args(self, index: int = 0) -> tuple[list, str] | None:
        text = self.text
        command = self.get_command(True)
        if text == None or command == None:
            return None
        else:
            text = text.replace(command, "").strip()
            if text == '':
                return None

            splitted = text.split()

            isplit = splitted[:index]

            for s in isplit:
                found = text.find(s)
                s_len = len(s)
                _r = text[found:s_len]
                _rplc = text.replace(_r, '')
                text = _rplc.strip()

            return isplit, text

# Tests
if __name__ == '__main__':
    import random
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
        try:
            print("=================")
            print(f"Text: {text}")
            parser = Parser(uname, text)
            cmd = parser.get_command()
            print(f"Command: {cmd}")
            args = parser.get_args(random.randint(-3,3))
            print(f"Args:{args}")
            print("=================")
            print("\n")
        except IndexError as e:
            print("Index Error caused by random.randint. It should be okay!")
            print(e)