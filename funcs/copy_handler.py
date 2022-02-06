from pyrogram import types, errors

async def main(msg: types.Message, *another):
    try:
        user = msg.from_user.id if msg.from_user else None
        if user == None:
            return await msg.reply("Saya tidak tau siapa Anda :v", True)
        if msg.reply_to_message == None:
            return await msg.reply("Reply ke suatu pesan biar ku copy ke pesan pribadimu!", True)
        return await msg.reply_to_message.copy(user)
    except errors.UserIsBlocked:
        return await msg.reply("Sayangnya kamu nge block saya :(", True)
    except errors.PeerIdInvalid:
        return await msg.reply("PM saya terlebih dahulu untuk menggunakan fitur ini :)", True)