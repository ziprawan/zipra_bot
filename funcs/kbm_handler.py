from pyrogram.errors import ChatAdminRequired, PeerIdInvalid, UserAdminInvalid, UsernameNotOccupied, UserNotParticipant
from pyrogram.types import Message, ChatPermissions, ChatMember, InlineKeyboardMarkup, InlineKeyboardButton
from utils.check_admin import main as checkAdmin
import logging


async def muting_handler(msg: Message, opsi, user):
    # Checking if user is my bot self
    me = await msg._client.get_me()
    if user.is_self == True:
        return await msg.reply("Saya gabisa mute saya sendiri")

    member_me = await msg.chat.get_member("me")
    if member_me.status != 'administrator':
        raise ChatAdminRequired
    # Handling mute and unmute
    if opsi == 'mute':
        permission = ChatPermissions(can_send_messages=False)
        try:
            await msg.chat.restrict_member(user.id, permission)
        except UserAdminInvalid:
            return await msg.reply("Admin tidak bisa saya mute!", True)
        return await msg.reply(f"<a href='tg://user?id={user.id}'>{user.first_name}</a> berhasil ku mute!", True)
    elif opsi == 'unmute':
        chat_permission = msg.chat.permissions
        permission = ChatPermissions(
            can_send_messages = True,
            can_send_media_messages = chat_permission.can_send_media_messages,
            can_send_stickers = chat_permission.can_send_stickers,
            can_send_animations = chat_permission.can_send_animations,
            can_use_inline_bots = chat_permission.can_use_inline_bots,
            can_add_web_page_previews = chat_permission.can_add_web_page_previews,
            can_send_polls = chat_permission.can_send_polls,
            can_change_info = chat_permission.can_change_info,
            can_invite_users = chat_permission.can_invite_users,
            can_pin_messages = chat_permission.can_pin_messages
        )
        try:
            await msg.chat.restrict_member(user.id, permission)
        except UserAdminInvalid:
            return await msg.reply("Admin tidak bisa saya unmute!", True)
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
    # Cek apakah di private
    if msg.chat.type == 'private': # Jika iya, tidak melakukan apapun
        return
    if msg.reply_to_message != None:
        if msg.reply_to_message.from_user == None:
            return await msg.reply("Menendang channel atau anonymous bukanlah ide yang bagus", True)
        else:
            return await kicking_handler(msg, msg.reply_to_message.from_user)
    elif msg.entities != None:
        for i in msg.entities:
            if i.type == 'mention':
                try:
                    user = await msg._client.get_users(msg.text[i.offset:i.offset + i.length])
                    await msg.reply("get_users passed")
                    await kicking_handler(msg, user)
                except UsernameNotOccupied:
                    return await msg.reply("Username tidak ditemukan!", True)
                except PeerIdInvalid:
                    return await msg.reply("Username tidak ditemukan!", True)
            elif i.type == 'text_mention':
                user = i.user
                await kicking_handler(msg, user)
            
    else:
        return await msg.reply("Reply atau mention ke user biar aku kick!", True)

async def kickme(msg: Message):
    ca = await checkAdmin(msg)
    if ca != False:
        return await msg.reply("Oh gabisa, U kan admin")
    
    member_me = await msg.chat.get_member("me")
    if member_me.can_restrict_members == False:
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
    # Check if chat type is private or not
    logging.info("mute: Checking Chat type...")
    if msg.chat.type == 'private': # Jika iya, tidak melakukan apapun
        return
    logging.info("mute: Checking Reply Message...")
    if msg.reply_to_message != None:
        logging.info("mute: Checking either channel/anonymous...")
        if msg.reply_to_message.from_user == None:
            logging.info("mute: channel/anonymous detected!")
            return await msg.reply("Uhh, saya gabisa mute anonim atau channel :v", True)
        else:
            logging.info("mute: User detected! Muting...")
            return await muting_handler(msg, 'mute', msg.reply_to_message.from_user)
    elif msg.entities != None:
        logging.info("mute: Reply Message not detected. Checking Entities...")
        for i in msg.entities:
            logging.info("mute: Entities found! Parsing for mention...")
            if i.type == 'mention':
                logging.info("mute: mention type detected!")
                try:
                    logging.info("mute: Checking user info...")
                    user = await msg._client.get_users(msg.text[i.offset:i.offset + i.length])
                except UsernameNotOccupied:
                    logging.ERROR("mute: Username Not Occupied!")
                    return await msg.reply("Username tidak ditemukan!", True)
                except PeerIdInvalid:
                    logging.ERROR("mute: Peer Id Invalid")
                    return await msg.reply("Username tidak ditemukan!", True)
                except IndexError:
                    logging.ERROR("mute: Index Error!")
                    return await msg.reply("Channel/Grup ndak bisa di mute banh", True)
                logging.info("mute: Muting...")
                await muting_handler(msg, 'mute', user)
                
            elif i.type == 'text_mention':
                logging.info("mute: text_mention type detected!")
                user = i.user
                logging.info("mute: Muting...")
                await muting_handler(msg, 'mute', user)
            else:
                logging.info("mute: Couldn't find mention types on entities :(")
                return await msg.reply("uhgesbgfrcyewgyjfgucyrdug")
    else:
        logging.info("mute: User not specified!")
        return await msg.reply("Reply atau mention ke user biar aku mute!", True)

async def unmute(msg: Message):
    if msg.chat.type == 'private':
        return
    if msg.reply_to_message != None:
        if msg.reply_to_message.from_user == None:
            return await msg.reply("Oke, unmute channel atau anonymous bukanlah suatu ide yang bagus", True)
        else:
            return await muting_handler(msg, 'unmute', msg.reply_to_message.from_user)
    elif msg.entities != None:
        for i in msg.entities:
            if i.type == 'mention':
                try:
                    user = await msg._client.get_users(msg.text[i.offset:i.offset + i.length])
                except UsernameNotOccupied:
                    return await msg.reply("Username tidak ditemukan!", True)
                except PeerIdInvalid:
                    return await msg.reply("Username tidak ditemukan!", True)
                await muting_handler(msg, 'unmute', user)
            elif i.type == 'text_mention':
                user = i.user
                await muting_handler(msg, 'unmute', user)
            
    else:
        return await msg.reply("Reply atau mention ke user biar aku unmute!", True)

async def main(msg: Message, command, args):
    print(command)
    print(1)
    if command == 'mute':
        print(2)
        return await mute(msg)
    elif command == 'unmute':
        print(3)
        return await unmute(msg)
    elif command == 'kickme':
        print(4)
        return await kickme(msg)
    elif command == 'kick':
        print(5)
        return await kick(msg)
    print(6)
