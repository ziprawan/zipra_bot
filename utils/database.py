import asyncio, ast

class DatabaseExecutorError(BaseException): ...

class MyDatabase:
    def __init__(self, database):
        self.path = f'databases/{database}'
    async def exec(self, cmd):
        PIPE = asyncio.subprocess.PIPE
        command = f'sqlite3 {self.path} ".mode json" "{cmd}"'
        print(command)
        executed = await asyncio.subprocess.create_subprocess_shell(command, True, PIPE, PIPE)
        stdout, stderr = await executed.communicate()
        if stderr != b'':
            raise DatabaseExecutorError(f"Error while executing sqlite command.\nError: {stderr.decode()}")
        return stdout.decode()
    async def get_data(self, cmd):
        out = await self.exec(cmd) # Example output: '[{1, "data1", "Text1"},\n{2, "data2", "Text2"}]\n'
        replaced = out.replace('\n', '') # Now should be: '[{1, "data1", "Text1"},{2, "data2", "Text2"}]'
        try:
            converted_to_list = ast.literal_eval(replaced) # Now type is list and iterable
        except SyntaxError:
            return [] # In case stdout is ''
        return converted_to_list
    
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