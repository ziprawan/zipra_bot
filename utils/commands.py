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
                    return splitted_with_prefix[1].lower()
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