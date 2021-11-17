from pyrogram.errors import ChatAdminRequired, PeerIdInvalid, UserAdminInvalid, UsernameNotOccupied, UserNotParticipant
from pyrogram.types import Message, ChatPermissions, ChatMember, InlineKeyboardMarkup, InlineKeyboardButton
from utils.check_admin import main as checkAdmin

async def muting_handler(msg: Message, opsi, user):
    # Checking if user is my bot self

    if user.id == msg._client.get_me().id:
        return await msg.reply("Saya gabisa mute saya sendiri")

    # Cek sudah termute atau belum
    try:
        perm: ChatMember = await msg.chat.get_member(user.id)
    except UserNotParticipant:
        return await msg.reply("User ini tidak ada di grup ini!", True)
    except:
        perm: ChatMember = await msg.chat.get_member(user.username)
    if await msg.chat.get_member("me").status != 'administrator':
        raise ChatAdminRequired
    else:
        is_muted = perm.can_send_messages
    # Handling mute and unmute
    if opsi == 'mute':
        if is_muted == True:
            return await msg.reply(f'Maaf, tapi {user.first_name} sudah termute', True)
        else:
            permission = ChatPermissions(can_send_messages=False)
            try:
                await msg.chat.restrict_member(user.id, permission)
            except UserAdminInvalid:
                return await msg.reply("Admin tidak bisa saya mute!", True)
            return await msg.reply(f"<a href='tg://user?id={user.id}'>{user.first_name}</a> berhasil ku mute!", True)
    elif opsi == 'unmute':
        if is_muted == False:
            return await msg.reply("Maaf, tapi {user.first_name} sudah terunmute", True)
        else:
            permission = ChatPermissions(can_send_messages=True)
            await msg.chat.restrict_member(user.id, permission)
            return await msg.reply(f"<a href='tg://user?id={user.id}'>{user.first_name}</a> berhasil ku unmute!", True)

async def kicking_handler(msg: Message, user):
    # Cek apakah ada user di grup itu atau tidak
    try:
        p = await msg.chat.get_member(user.id)
    except PeerIdInvalid:
        p = await msg.chat.get_member(user.username)
    except:
        return await msg.reply("Wah wah wah, dia ga ada disini kok minta di kick :v", True)
    
    kicked = await msg.chat.kick_member(p.user.id)
    await kicked.delete()
    await msg.chat.unban_member(p.user.id)
    return await msg.reply(f'<a href=\'tg://user?id={p.user.id}\'>{p.user.first_name}</a> berhasil aku kick!', True)

async def kick(msg):
    pass

async def kickme(msg: Message):
    ca = await checkAdmin(msg)
    if ca != False:
        return await msg.reply("Oh gabisa, U kan admin")
    
    if await msg.chat.get_member("me").can_restrict_members == False:
        raise ChatAdminRequired

    return await msg.reply("Apakah Anda yakin ingin menendang diri Anda sendiri?",
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

async def ban(msg):
    pass

async def mute(msg: Message):
    # Cek apakah di private
    if msg.chat.type == 'private': # Jika iya, tidak melakukan apapun
        return
    if msg.reply_to_message != None:
        if msg.reply_to_message.from_user == None:
            return await msg.reply("Uhh, saya gabisa mute anonim atau channel :v", True)
        else:
            return await muting_handler(msg, 'mute', msg.reply_to_message.from_user)
    elif msg.entities != None:
        for i in msg.entities:
            if i.type == 'mention':
                try:
                    user = await msg._client.get_users(msg.text[i.offset:i.offset + i.length])
                except UsernameNotOccupied:
                    return await msg.reply("Username tidak ditemukan!", True)
                await muting_handler(msg, 'mute', user)
                break
            elif i.type == 'text_mention':
                user = i.user
                await muting_handler(msg, 'mute', user)
                break
    else:
        return await msg.reply("Reply atau mention ke user biar aku mute!", True)

async def main(msg: Message, command, args):
    if command == 'mute':
        return await mute(msg)
    elif command == 'kickme':
        return await kickme(msg)
