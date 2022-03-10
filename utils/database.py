import asyncio, ast

class DatabaseExecutorError(BaseException): ...

class MyDatabase:
    def __init__(self, database):
        self.path = f'databases/{database}'
    async def exec(self, cmd):
        PIPE = asyncio.subprocess.PIPE
        command = f'sqlite3 {self.path} ".mode list" ".header on" "{cmd}"'
        executed = await asyncio.subprocess.create_subprocess_shell(command, True, PIPE, PIPE)
        stdout, stderr = await executed.communicate()
        if stderr != b'':
            raise DatabaseExecutorError(f"Error while executing sqlite command.\nError: {stderr.decode()}")
        return stdout.decode()
    async def get_data(self, cmd):
        out = await self.exec(cmd)
        get_data_result = []

        splitted_by_newline = out.splitlines()
        var_names = splitted_by_newline[0].split("|") 
        print(var_names)
        splitted_by_newline.pop(0) 
        splitted_by_newline.pop(-1) 

        if splitted_by_newline == []:
            print(1)
            return splitted_by_newline

        for splitted in splitted_by_newline:
            splitted_by_vertical_bar = splitted.split("|")
            tmp = {}
            for i in range(len(var_names)):
                tmp[var_names[i]] = splitted_by_vertical_bar[i]

            get_data_result.append(tmp)

        return get_data_result
    
    @staticmethod
    def format(text: str):
        if not isinstance(text, str):
            raise ValueError(f"excpected str, got {type(text)}")
        
        p = "'"
        new_text = p

        for i in text:
            tmp = i
            if i == p:
                tmp = i*2
            new_text += tmp
        
        new_text += p
        return new_text
    
    @staticmethod
    def stringify(text: str):
        return format(text)