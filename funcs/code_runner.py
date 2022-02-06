from pyrogram.types import Message
import aiohttp, configparser

langs = {
    'assembly': 'asm',
    'ats': 'ats',
    'bash': 'sh',
    'c': 'c',
    'clojure': 'clj',
    'cobol': 'cbl',
    'coffeescript': 'coffee',
    'cpp': 'cpp',
    'crystal': 'cr',
    'csharp': 'cs',
    'd': 'd',
    'elixir': 'ex',
    'elm': 'elm',
    'erlang': 'erl',
    'fsharp': 'fs',
    'go': 'go',
    'groovy': 'groovy',
    'haskell': 'hs',
    'idris': 'idr',
    'java': 'java',
    'javascript': 'js',
    'julia': 'jl',
    'kotlin': 'kt',
    'lua': 'lua',
    'mercury': 'm',
    'nim': 'nim',
    'nix': 'nix',
    'ocaml': 'ml',
    'perl': 'pl',
    'php': 'php',
    'python': 'py',
    'raku': 'raku',
    'ruby': 'rb',
    'rust': 'rs',
    'scala': 'scala',
    'swift': 'swift',
    'typescript': 'ts'
}

async def main(msg: Message, cmd, args):
    config = configparser.ConfigParser()
    config.read('config.ini')
    glot_api = config['configs']['glot_api']

    if args == None:
        if msg.reply_to_message == None:
            return await msg.reply(f"Tolong masukkan kode {cmd}nya!")
        else:
            rtm = msg.reply_to_message
            args = rtm.text if rtm.text else rtm.caption
            if args == None:
                return await msg.reply(f"Tolong masukkan kode {cmd}nya!")

    header = {
        'Authorization': 'Token ' + glot_api,
        'Content-type': 'application/json'
    }
    async with aiohttp.ClientSession(headers=header) as session:
        data = {
            'files': [
                {
                    'name': 'zipra_bot.' + langs[cmd],
                    'content': args
                }
            ]
        }
        async with session.post('https://glot.io/api/run/' + cmd + '/latest', json=data) as result:
            status = result.status
            dump = await result.json()
            if status != 200:
                return await msg.reply(f"Server memberikan kode http yg tidak valid. HTTP Code: <a href=\"https://http.cat/{status}\">///ll⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣</a>{status}", True)
            else:
                stdout = dump['stdout']
                error = dump['error']
                stderr = dump['stderr']
                if stdout == '' and error != '':
                    # Eksekusi kode error
                    message = stderr.replace('glot', 'aziz', 1)
                elif stdout != '' and error == '':
                    message = stdout.replace('glot', 'aziz', 1)
                else:
                    message = "```No Output!```"
                if len(message) < 4096:
                    return await msg.reply(message, True)
                else:
                    filename = f"zipra.{langs[cmd]}.txt"
                    with open(filename, 'w') as file:
                        file.write(message)
                    await msg.reply_document(filename, True)
                    import os
                    if os.path.exists(filename):
                        return os.remove(filename)
                    return True
