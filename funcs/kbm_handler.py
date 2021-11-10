from pyrogram.errors import ChatAdminRequired, PeerIdInvalid
from pyrogram.types import Message, ChatPermissions, ChatMember, InlineKeyboardMarkup, InlineKeyboardButton
from utils.check_admin import main as checkAdmin

def muting_handler(msg: Message, opsi, user):
    # Cek sudah termute atau belum
    try:
        perm: ChatMember = msg.chat.get_member(user.id)
    except:
        perm: ChatMember = msg.chat.get_member(user.username)
    if perm.can_send_messages == None:
        raise ChatAdminRequired
    else:
        is_muted = not perm.can_send_messages

    # Handling mute and unmute
    if opsi == 'mute':
        if is_muted == True:
            return msg.reply(f'Maaf, tapi {user.first_name} sudah termute', True)
        else:
            permission = ChatPermissions(can_send_messages=False)
            msg.chat.restrict_member(user.id, permission)
            return msg.reply(f"<a href='tg://user?id={user.id}'>{user.first_name}</a> berhasil ku mute!", True)
    elif opsi == 'unmute':
        if is_muted == False:
            return msg.reply("Maaf, tapi {user.first_name} sudah terunmute", True)
        else:
            permission = ChatPermissions(can_send_messages=True)
            msg.chat.restrict_member(user.id, permission)
            return msg.reply(f"<a href='tg://user?id={user.id}'>{user.first_name}</a> berhasil ku unmute!", True)

def kicking_handler(msg: Message, user):
    # Cek apakah ada user di grup itu atau tidak
    try:
        p = msg.chat.get_member(user.id)
    except PeerIdInvalid:
        p = msg.chat.get_member(user.username)
    except:
        return msg.reply("Wah wah wah, dia ga ada disini kok minta di kick :v", True)
    
    msg.chat.kick_member(p.user.id)
    msg.chat.unban_member(p.user.id)
    return msg.reply(f'<a href=\'tg://user?id={p.user.id}\'>{p.user.first_name}</a> berhasil aku kick!', True)

def kick(msg):
    pass

def kickme(msg: Message, bot):
    ca = checkAdmin(msg)
    if ca != False:
        return msg.reply("Oh gabisa, U kan admin")
    
    if msg.chat.get_member("me").can_restrict_members == False:
        raise ChatAdminRequired

    return msg.reply("Apakah Anda yakin ingin menendang diri Anda sendiri?",
    True,
    reply_markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("✅ Iya", callback_data=f"/kick {msg.from_user.id}"),
                InlineKeyboardButton("❌ Tidak", callback_data=f"/kickgajadi {msg.from_user.id}")
            ]
        ]
    )
    )

def ban(msg):
    pass

def mute(msg: Message, bot):
    # Cek apakah di private
    if msg.chat.type == 'private': # Jika iya, tidak melakukan apapun
        return
    if msg.reply_to_message != None:
        if msg.reply_to_message.from_user == None:
            return msg.reply("Uhh, saya gabisa mute anonim atau channel :v", True)
        else:
            ca = checkAdmin(msg.reply_to_message)
            if ca != False:
                return msg.reply("Saya gabisa mute admin")
            else:
                return muting_handler(msg, 'mute', msg.reply_to_message.from_user)
    elif msg.entities != None:
        for i in msg.entities:
            if i.type == 'mention':
                user = bot.get_users(msg.text[i.offset:i.offset + i.length])
                muting_handler(msg, 'mute', user)
            elif i.type == 'text_mention':
                user = i.user
                muting_handler(msg, 'mute', user)
            break

def main(msg: Message, bot, command, args):
    if command == 'mute':
        return mute(msg, bot)
    elif command == 'kickme':
        return kickme(msg, bot)
