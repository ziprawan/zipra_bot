import os

async def main(msg, *another):
    if len(str(msg)) < 4096:
        return await msg.reply(f'<code>{msg}</code>')
    json_file = open('result.txt', 'w')
    json_file.write(str(msg))
    json_file.close()
    await msg.reply_document('result.txt', True, caption="Result")
    if os.path.exists('result.txt'):
        os.remove('result.txt')
