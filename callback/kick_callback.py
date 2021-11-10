from pyrogram.types import CallbackQuery
from funcs.kbm_handler import kicking_handler as kick

def main(msg: CallbackQuery, bot, command, args):
    if command == 'kick':
        if msg.data.split(' ')[1] != str(msg.from_user.id):
            return msg.answer("Bukan untuk kamu", True)
        user = bot.get_users(args)
        kick(msg.message, user)
        return msg.message.delete()
    elif command == 'kickgajadi':
        if msg.data.split(' ')[1] != str(msg.from_user.id):
            return msg.answer("Bukan untuk kamu", True)
        return msg.message.delete()
    else:
        pass