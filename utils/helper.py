# ---------- Import needed libs ----------
import struct
from telethon.tl.custom.message import Message
from telethon import TelegramClient, functions, types, _ as patched, errors
from datetime import timedelta
from .lang import Language

# ---------- Variables ----------
default_admin_perm = {
    'view_messages': True,
    'send_games': True,
    'send_gifs': True,
    'send_inline': True,
    'send_media': True,
    'send_polls': True,
    'send_stickers': True,
    'send_messages': True,
    'embed_links': True
}


# ---------- Classes ----------
class Default(dict):
    def __missing__(self, key):
        return '{' + key + '}'


# ---------- Async functions ----------

async def check_admin(event: Message, chat: types.TypeInputChannel = None, user: types.TypeInputPeer = None):
    status = await check_status(event, chat, user)
    privilege = ['admin', 'creator', 'anonym', 'private']
    if status in privilege:
        return True
    else:
        return False


async def check_perm(event: Message, perm: str, chat: types.TypeChat | None = None,
                     user: types.TypeInputPeer | None = None):
    permissions = await get_perm(event, chat, user)
    if perm in permissions:
        return permissions[perm]
    else:
        raise KeyError("Permission not found")


async def get_perm(event: Message, chat: types.TypeChat | None = None, user: types.TypePeer | None = None):
    # RAISE ERROR IF CHAT TYPE IS PRIVATE
    if event.is_private:
        raise TypeError("There is no permission in private chat")

    # Declare some needed variables
    chat = chat if chat else (await event.get_chat())
    user = user if user else (await event.get_sender())
    # permissions list. All default None. Will be declared after parsing participant info
    permissions = {
        'add_admins': None,
        'anonymous': None,
        'ban_users': None,
        'change_info': None,
        'delete_messages': None,
        'edit_messages': None,
        'embed_links': None,
        'invite_users': None,
        'manage_call': None,
        'other': None,
        'pin_messages': None,
        'post_messages': None,
        'send_games': None,
        'send_gifs': None,
        'send_inline': None,
        'send_messages': None,
        'send_media': None,
        'send_polls': None,
        'send_stickers': None,
        'view_messages': None,
    }
    # Types list
    admins = (types.ChannelParticipantCreator, types.ChannelParticipantAdmin)
    member = types.ChannelParticipant
    banned = types.ChannelParticipantBanned
    # Get participant request info
    try:
        get_participant_result: types.channels.ChannelParticipant = await event.client(
            functions.channels.GetParticipantRequest(
                channel=chat,
                participant=user
            ))
        participant = get_participant_result.participant
    except errors.UserNotParticipantError:
        participant = member(0, None)

    if isinstance(participant, admins):
        user_perm = participant.admin_rights
        user_perm = user_perm.to_dict()
        user_perm.pop('_')
        permissions.update(user_perm)
        permissions.update(default_admin_perm)

    elif isinstance(participant, (banned, member)):
        if isinstance(participant, banned):
            user_perm = participant.banned_rights
        else:
            user_perm = chat.default_banned_rights

        user_perm = user_perm.to_dict()
        user_perm.pop('_')
        for key, value in user_perm.items():
            permissions.update({key: None if value is True else value})

    return permissions


async def check_status(event: Message, chat: types.TypeInputChannel = None, user: types.TypeInputPeer = None):
    """My helper to check_status of sender.
    Should return 'private' if in private,
    'member' if user is member of chat,
    'admin' if user is admin of chat,
    'creator' if user is owner of chat,
    'resticted' if user is restricted,
    'channel' if user is linked channel,
    'anonym' if admin sent as anonymous
    'anonch' if user is sent as channel"""
    if event.is_private:
        # On Private chat. Return private
        return "private"
    else:
        chat = await event.get_chat() if chat is None else chat
        user = await event.get_input_sender() if user is None else user
        if isinstance(user, patched.User):
            # Sender is user, check member or admin or owner
            try:
                get_participant_result: types.channels.ChannelParticipant = await event.client(
                    functions.channels.GetParticipantRequest(
                        channel=chat,
                        participant=user
                    ))
            except errors.UserNotParticipantError:
                return "member"
            participant = get_participant_result.participant
            if isinstance(participant, types.ChannelParticipant):
                return "member"
            elif isinstance(participant, types.ChannelParticipantAdmin):
                return "admin"
            elif isinstance(participant, types.ChannelParticipantCreator):
                return "creator"
            elif isinstance(participant, types.ChannelParticipantBanned):
                return "restricted"
        elif isinstance(user, types.Channel):
            if user.megagroup:
                return "anonym"
            full: types.messages.ChatFull = await event.client(functions.channels.GetFullChannelRequest(
                channel=await event.get_input_chat()
            ))
            linked_chat_id = full.full_chat.linked_chat_id
            user_id = user.id
            if user_id == linked_chat_id:
                return "channel"
            else:
                return "anonch"


async def get_user(event: Message, user: str | int):
    full_user: types.users.UserFull = await event.client(functions.users.GetFullUserRequest(
        id=user
    ))
    return full_user.users[0]


async def send_sticker(client: TelegramClient, peer: types.TypeInputPeer, sticker_id: int, access_hash: int,
                       file_reference: bytes, messages: str = "", silent: bool | None = None,
                       reply_to_msg_id: int | None = None):
    """My helper to simplify send sticker process :)"""
    return await client(functions.messages.SendMediaRequest(
        peer=peer,
        media=types.InputMediaDocument(
            id=types.InputDocument(
                id=sticker_id,
                access_hash=access_hash,
                file_reference=file_reference
            )
        ),
        message=messages,
        silent=silent,
        reply_to_msg_id=reply_to_msg_id
    ))


async def get_multi_lang_num(lang: Language, num: int, str_name: str):
    """My helper to simplify get_multi_lang_num process :)"""
    if num == 0:
        _msg = ""
    elif num == 1 or abs(num) == 1:
        _msg = await lang.get('one_' + str_name)
    elif num == 2 or abs(num) == 2:
        _msg = await lang.get('two_' + str_name)
    else:
        _msg = await lang.get('more_' + str_name)

    return _msg


# ---------- End async functions ----------
# ---------- Sync functions ----------

def convert_seconds(time):
    """
    Convert seconds to hours, minutes and seconds.
    """
    time_delta = timedelta(seconds=time)
    days = time_delta.days
    hours = time_delta.seconds // 3600
    minutes = time_delta.seconds % 3600 // 60
    seconds = time_delta.seconds % 3600 % 60
    return days, hours, minutes, seconds


def add_surrogate(text):
    """Adding surrogate to the text.
    SMP -> Surrogate Pairs (Telegram offsets are calculated with these).
    See https://en.wikipedia.org/wiki/Plane_(Unicode)#Overview for more.
    
    Big thanks to telethon dev!"""
    return "".join(
        "".join(
            chr(y) for y in struct.unpack("<HH", x.encode("utf-16le"))
        ) if (0x10000 <= ord(x) <= 0x10FFFF)
        else x
        for x in text
    )


def get_length(text):
    """Count Length of text with surrogate addition"""
    return len(add_surrogate(text))


def ol_generator(text: str, var: list, res: list):
    """My helper for offset and length generator for formatting_entities"""
    offsets = []
    lengths = []

    if isinstance(var, list) and isinstance(res, list):
        if len(var) != len(res):
            return None

        for i in range(len(var)):
            var[i] = '{' + var[i] + '}'

        for i in res:
            lengths.append(get_length(str(i)))

        for j in range(len(lengths)):
            tmp = get_length(text[:text.find(var[j])])
            if j != 0:
                add, subtract = 0, 0
                for k in range(j):
                    add += get_length(str(res[k]))
                    subtract += get_length(var[k])
                tmp += add - subtract
            offsets.append(tmp)

        return offsets, lengths
    else:
        return None

# ---------- End sync functions ----------
