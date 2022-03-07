from multiprocessing.sharedctypes import Value
from typing import List
import time, inspect
from utils.helper import Default, check_perm, get_user, ol_generator, send_sticker
from utils.lang import Language
from telethon.tl.custom.message import Message
from telethon.sync import TelegramClient, errors
from telethon.tl.types import (
    Channel,
    InputMessageEntityMentionName,
    InputUser,
    MessageEntityCode,
    TypePeer,
    InputPeerSelf
)

# async def ban(event: Message, lang: Language, user: TypePeer|List[TypePeer], reason: str):
#     chat = await event.get_chat()
#     client: TelegramClient = event.client

#     if isinstance(user, list):
#         success, failed = 0, 0
#         for usr in user:
#             try:
#                 await client.edit_permissions(
#                     chat,
#                     usr,
#                     0,
#                     view_messages=False
#                 )
#                 success += 1
#             except errors.UserAdminInvalidError:
#                 failed += 1
#         return await event.reply(
#             (await lang.get('restrict_batch')).format_map(Default(
#                 action = "Ban",
#                 success = str(success),
#                 failed = str(failed),
#                 reason = str(reason)
#             ))
#         )

#     try:
#         await client.edit_permissions(
#             chat,
#             user,
#             0,
#             view_messages=False
#         )
#     except errors.UserAdminInvalidError:
#         return await event.reply(
#             (await lang.get('restrict_admin_error')).format_map(Default(action="ban"))
#         )
#     # if ban_result.updates != []:
#     #     await client.delete_messages(chat, ban_result.updates[0])
#     string: str = await lang.get('banned')
#     vars = ['name']
#     res = [user.title if isinstance(user, Channel) else user.first_name]
    
#     if reason != None:
#         string += '\n' + await lang.get('reason')
#         vars.append('reason')
#         res.append(reason)

#     offs, lens = ol_generator(string, vars, res)
#     await send_sticker(
#         client, 
#         chat, 
#         6080049489123476920, 
#         -8737819976689190729, 
#         b'\x02_U\xfe\x0e\x00\x00M\xb5b\x0b4\xf3\xbd\xebR\xa9\xf1<=\xac\x94nt\xebG\xe2\x08\xa9',
#         "Hahahaha, got banned!",
#         False)
#     await event.respond(
#         string.format_map(Default(name=res[0], reason=reason)),
#         formatting_entities = [InputMessageEntityMentionName(
#             offset = offs[0],
#             length = lens[0],
#             user_id = InputUser(
#                 user_id = user.id,
#                 access_hash = user.access_hash
#             )
#         )]
#     )

async def bans(client: TelegramClient, chat, user: TypePeer, ban = True):
    if ban == True:
        r = None
    else:
        r = True
    try:
        await client.edit_permissions(
            chat, user, 0,
            view_messages = r
        )
        return True
    except errors.UserAdminInvalidError:
        return False        
    

async def ban(event: Message, lang: Language, user: str|int|list[str|int], reason: str):
    chat = await event.get_chat()
    entities = []
    error_msg = ""

    if isinstance(user, list):
        success, failed = 0, 0
        for u in user:
            try:
                usr = await get_user(event, u)
                result = await bans(event.client, chat, usr)
                if result == True:
                    success += 1
                else:
                    failed += 1
            except ValueError as v:
                error_msg += str(v) + '\n'
                failed += 1
        if error_msg != "":
            await event.respond(error_msg)
        msg = (await lang.get('restrict_batch')).format_map(Default(action="Ban", success=str(success), failed=str(failed)))
        return await event.respond(msg)
    else:
        try:
            result = await bans(event.client, chat, user)
        except ValueError as e:
            error_msg = str(e)
            return await event.respond(error_msg)
        if result == True:
            msg = await lang.get('banned')
            var = ['name']
            res = [user.first_name]
            offs, lens = ol_generator(msg, var, res)
            msg = msg.format(name=res[0])
            entities = [InputMessageEntityMentionName(offset=offs[0], length=lens[0], user_id=InputUser(user_id=user.id, access_hash=user.access_hash))]
        else:
            msg = await lang.get('restrict_admin_error')
            msg = msg.format(action=inspect.stack()[0].function)
            entities = []
        return await event.respond(msg, formatting_entities=entities)
        

async def unban(event: Message, lang: Language, user: TypePeer):
    chat = await event.get_chat()
    client: TelegramClient = event.client

    edit_permission_result = await client.edit_permissions(
        entity = chat,
        user = user,
        until_date = 0,
        view_messages = True
    )

    message = await lang.get('unbanned')
    var = ['name']
    res = [user.title if isinstance(user, Channel) else user.first_name]
    offs, lens = ol_generator(message, var, res)

    return await event.reply(
        message.format_map(Default(name=res[0])),
        formatting_entities = [InputMessageEntityMentionName(
            offset = offs[0],
            length = lens[0],
            user_id = InputUser(
                user_id = user.id,
                access_hash = user.access_hash
            )
        )]
    )

async def nban(event: Message, lang: Language, user: TypePeer, reason: str):
    pass

async def main(*args):
    event: Message = args[0]
    lang = Language(event)

    # Check private
    if event.is_private:
        return await event.reply(await lang.get('private_error'))

    parser = args[1]
    param: str = await parser.get_options()
    cmd = await parser.get_command()
    can_ban_user = await check_perm(event, 'ban_users')
    i_can_ban = await check_perm(event, 'ban_users', user=InputPeerSelf())

    # Check permissions
    if not i_can_ban:
        msg = await lang.get('i_missing_perms')
        offs, lens = ol_generator(msg, ['perm'], ['ban_users'])
        return await event.reply(
            msg.format_map(Default(perm="ban_users")),
            formatting_entities = [MessageEntityCode(
                offset = offs[0],
                length = lens[0]
            )]
        )
    if not can_ban_user:
        msg = await lang.get('missing_perms')
        offs, lens = ol_generator(msg, ['perm'], ['ban_users'])
        return await event.reply(
            msg.format_map(Default(perm="ban_users")),
            formatting_entities = [MessageEntityCode(
                offset = offs[0],
                length = lens[0]
            )]
        )

    # Getting user
    replied = await event.get_reply_message()
    if replied:
        user = await replied.get_sender()
        reason = param if param == None else param.split()
    else:
        if param:
            splitted = param.split(' ')
            tmp = splitted[0]
            if '\n' in tmp:
                tmp = tmp.split('\n')
            reason = param.replace(tmp, '', 1).strip()
            user = []
            if ',' in tmp:
                for i in tmp.split(','):
                    if i != '':
                        user.append(int(i) if i.isdigit() else i)
            else:
                user = int(tmp) if tmp.isdigit() else tmp
        else:
            return await event.reply((await lang.get('not_replied')).format(action=cmd))

    if cmd == "ban":
        return await ban(event, lang, user, reason)
    elif cmd == "unban":
        return await unban(event, lang, user)
    elif cmd == "nban":
        return await nban(event, lang, user)
    # elif cmd == "kick":
    #     return await kick(event, lang, user, reason)
