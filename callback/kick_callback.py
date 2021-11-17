from pyrogram.types import CallbackQuery
from funcs.kbm_handler import kicking_handler as kick

async def main(msg: CallbackQuery, command, args):
    if msg.data.split(' ')[1] != str(msg.from_user.id):
        return await msg.answer("Bukan untuk kamu", True)
        
    if command == 'kick':
        user = await msg._client.get_users(args)
        await kick(msg.message, user)
        return await msg.message.delete()
    elif command == 'kickgajadi':
        return await msg.message.delete()
    else:
        pass