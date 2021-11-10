from pyrogram.types import Message, ChatMember
from pyrogram import Client

def unpin_all(bot: Client, msg: Message) -> bool:
    result = bot.unpin_all_chat_messages(msg.chat.id)
    msg.reply("Semua pesan yg di pin berhasil di unpin!")
    return result

def unpin_msg(bot: Client, msg: Message) -> bool:
    chat = bot.get_chat(msg.chat.id)
    if msg.reply_to_message != None:
        msg.reply_to_message.unpin()
        msg.reply("Berhasil unpin pesan yg kau reply!", True)
        return True
    bot.unpin_chat_message(msg.chat.id, chat.pinned_message.message_id)
    msg.reply("Berhasil di unpin pesan!", True)
    return True

def pin_msg(msg: Message) -> bool:
    if msg.reply_to_message == None:
        msg.reply("Balas ke suatu pesan agar ku pin", True)
    else:
        msg.reply_to_message.pin(True)
        msg.reply("Pesan berhasil di pin!")

def pin_loud(msg: Message) -> bool:
    if msg.reply_to_message == None:
        msg.reply("Balas ke suatu pesan agar ku pin", True)
    else:
        msg.reply_to_message.pin()
        msg.reply("Pesan ini sudak aku pin dan ku kasih tau ke yg lain!")

def main(msg: Message, bot, cmd: str, args: str) -> bool:
    # Jika bukan anonymous 
    if msg.sender_chat != None:
        if msg.sender_chat.type == "channel":
            return msg.reply("Oh, you can't to do this 🗿", True)
    else:
        user = bot.get_chat_member(msg.chat.id, msg.from_user.id)
        if user.status != "administrator" and user.status != "creator":
            return msg.reply("Maaf, anda harus menjadi admin untuk melakukan ini :/", True)
    if cmd == 'pin':
        if args == None:
            pin_msg(msg)
        elif args == 'loud':
            pin_loud(msg)
        else:
            msg.reply("<code>Parameter is invalid!</code>", True)
    elif cmd == 'unpin':
        if args == None:
            unpin_msg(bot, msg)
        elif args == 'all':
            unpin_all(bot, msg)
        else:
            msg.reply("<code>Parameter is invalid!</code>", True)
    else:
        msg.reply("<code>Something went wrong!</code>", True)