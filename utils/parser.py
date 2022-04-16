class Args:
    def __init__(self, raw_text: str | None, splitted=None, replaced: str = "") -> None:
        if splitted is None:
            splitted = []
        self.raw_text = raw_text
        self.splitted: list[str] = splitted
        self.replaced = replaced

    def cut(self, index: int) -> "Args" or None:
        _text = self.raw_text
        if _text is None:
            return
        splitted = _text.split()

        isplit = splitted[:index]

        for s in isplit:
            found = _text.find(s)
            s_len = len(s)
            _r = _text[found:s_len]
            _rplc = _text.replace(_r, '')
            _text = _rplc.strip()

        self.splitted = splitted
        self.replaced = _text

        r = self.__class__(self.raw_text, splitted, _text)

        return r


class CallbackParser:
    def __init__(self, cdata: str | bytes):
        if isinstance(cdata, bytes):
            cdata = cdata.decode()
        if not isinstance(cdata, str):
            raise TypeError(f"We need 'str' type, not {type(cdata)}!")
        # Ex. pin_1234567890_loud
        splitted = cdata.split('_', 2)  # ['pin', '1234567890', 'loud']
        self.command = splitted[0]
        self.user_id = int(splitted[1])
        self.args = splitted[2]


class Parser:
    def __init__(self, username: str, msg: str) -> None:
        self.uname = username.lower()
        self.text = msg
        self.prefix = ['/', '!', '$', '\\']

    def get_command(self, return_bot_command: bool = False) -> str | None:
        message: str = self.text  # Example: /start@test_bot args
        if message is None:
            return None
        username = self.uname
        prefix = self.prefix
        if message[0] in prefix:
            if '\n' in message:
                splitted = message.splitlines()
                if ' ' in splitted[0]:
                    splitted = splitted[0].split()
            else:
                splitted = message.split()

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

    def get_args(self) -> Args:
        arg_text = self.text
        command = self.get_command(True)
        if arg_text is None or command is None:
            return Args(self.text)
        else:
            arg_text = arg_text.replace(command, "", 1).strip()
            if arg_text == '':
                return Args(None)
            return Args(arg_text)
