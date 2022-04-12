import inspect
from utils.database import Database
from utils.helper import Default, check_perm, get_user, ol_generator, get_multi_lang_num
from utils.lang import Language
from utils.parser import Parser

from telethon.tl.custom.message import Message
from telethon.tl.patched import User
from telethon.sync import TelegramClient, errors
from telethon.tl.types import (
    InputMessageEntityMentionName,
    InputUser,
    MessageEntityCode,
    TypePeer,
    User,
    InputPeerSelf,
    Channel,
    MessageEntityTextUrl,
)


async def bans(client: TelegramClient, chat: TypePeer, user: TypePeer | User | Channel, is_unban: bool | None = None):
    try:
        await client.edit_permissions(
            entity=chat,
            user=user,
            view_messages=is_unban
        )
        return True
    except errors.UserAdminInvalidError:
        return False


async def ban(event: Message, cmd: str, lang: Language, user: list[User | Channel], reason: str):
    _client = event.client
    _chat = await event.get_chat()
    _user = user
    _error = []
    _success = []

    for _u in user:
        ban_result = await bans(_client, _chat, _u, True if cmd == 'unban' else None)
        if ban_result is False:
            _error.append(_u)
        else:
            _success.append(_u)

    _msg_success = await get_multi_lang_num(lang, len(_success), 'banned' if cmd == 'ban' else 'unbanned')
    _msg_error = await get_multi_lang_num(lang, len(_error), 'restrict_admin_error')
    _msg_reason = await lang.get('reason')
    _all = _success + _error

    _msg_tmp = _msg_success.format(
        n=len(_success),
        users=", ".join("{user" + str(_) + "}" for _ in range(len(_success)))
    ) + "\n" + _msg_error.format(
        n=len(_error),
        users=", ".join("{user" + str(_) + "}" for _ in range(len(_success), len(_all)))
    ) + "\n" + (_msg_reason if reason else "")

    offs, lens = ol_generator(
        _msg_tmp,
        [f'user{i}' for i in range(len(_all))],
        [str(u.title if hasattr(u, 'title') else u.first_name) for u in _all]
    )

    _msg = _msg_success.format(
        n=len(_success),
        users=", ".join(str(u.title if hasattr(u, 'title') else u.first_name) for u in _success)
    ) + "\n" + _msg_error.format(
        n=len(_error),
        users=", ".join(str(u.title if hasattr(u, 'title') else u.first_name) for u in _error)
    ) + "\n" + (_msg_reason.format(reason=reason) if reason else "")

    entities = []

    for i in range(len(_all)):
        if isinstance(_all[i], Channel):
            entities.append(MessageEntityTextUrl(
                offset=offs[i],
                length=lens[i],
                url=f'https://t.me/{_all[i].username}'
            ))
        entities.append(InputMessageEntityMentionName(
            offset=offs[i],
            length=lens[i],
            user_id=InputUser(
                user_id=_all[i].id,
                access_hash=_all[i].access_hash
            )
        ))

    return await event.reply(
        _msg,
        formatting_entities=entities,
        link_preview=None
    )


async def nban(event: Message, lang: Language, user: TypePeer, reason: str):
    # Temp
    chat = await event.get_chat()
    entities = []
    error_msg = ""
    db = Database('groups', 'nban')


async def main(*args):
    event: Message = args[0]
    client: TelegramClient = event.client
    lang = Language(event)
    _user_error = []

    # Check private
    if event.is_private:
        return await event.reply(await lang.get('private_error'))

    parser: Parser = args[1]
    param = parser.get_args()
    cmd: str = parser.get_command()
    can_ban_user = await check_perm(event, 'ban_users')
    i_can_ban = await check_perm(event, 'ban_users', user=InputPeerSelf())

    # Check permissions
    if not i_can_ban or not can_ban_user:
        if not i_can_ban:
            msg = await lang.get('i_missing_perms')
        elif not can_ban_user:
            msg = await lang.get('missing_perms')
        else:
            msg = ""
        offs, lens = ol_generator(msg, ['perm'], ['ban_users'])
        return await event.reply(
            msg.format_map(Default(perm="ban_users")),
            formatting_entities=[MessageEntityCode(
                offset=offs[0],
                length=lens[0]
            )]
        )

    # Getting user
    replied: Message = await event.get_reply_message()
    if replied:
        users = await replied.get_sender()
        reason = param if param is None else param.raw_text
    else:
        if param.raw_text is None:
            return await event.reply((await lang.get('not_replied')).format(action=cmd))
        else:
            param = param.cut(1)
            _users = list(set(param.splitted[0].split(',')))
            users = []
            for u in _users:
                try:
                    users.append(await client.get_entity(u))
                except ValueError:
                    if u not in _user_error:
                        _user_error.append(str(u))
            reason = param.replaced

    if cmd == "ban" or cmd == "unban":
        await ban(event, cmd, lang, users, reason)
    elif cmd == "nban":
        await nban(event, lang, users, reason)
    # elif cmd == "kick":
    #     return await kick(event, lang, user, reason)

    # For user not found error
    _l_u_e = len(_user_error)
    if _l_u_e == 0:
        return
    else:
        if _l_u_e == 1:
            msg = await lang.get('one_user_not_found')
        elif _l_u_e == 2:
            msg = await lang.get('two_user_not_found')
        else:
            msg = await lang.get('more_user_not_found')

        _j = " ".join(_user_error).strip()
        offs, lens = ol_generator(msg, ['user'], [_j])
        return await event.respond(
            msg.format(user=_j),
            formatting_entities=[MessageEntityCode(
                offset=offs[0],
                length=lens[0]
            )]
        )
