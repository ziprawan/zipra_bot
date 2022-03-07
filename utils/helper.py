# ---------- Import needed libs ----------
import struct
from telethon.tl.custom.message import Message
from telethon import TelegramClient, functions, types, _ as patched, errors

# ---------- Classes ----------
class Default(dict):
    def __missing__(self, key):
        return '{'+key+'}'

# ---------- Async functions ----------

async def check_admin(event: Message, chat: types.TypeInputChannel = None, user: types.TypeInputPeer = None):
    status = await check_status(event, chat, user)
    privilege = ['admin', 'creator', 'anonym', 'private']
    if status in privilege:
        return True
    else:
        return False

async def check_perm(event: Message, perm: str, chat: types.TypeChat|None = None, user: types.TypePeer|None = None):
    permissions = await get_perm(event, chat, user)
    if perm in permissions:
        return permissions[perm]
    else:
        raise KeyError("Permission not found")

async def get_perm(event: Message, chat: types.TypeChat|None = None, user: types.TypePeer|None = None):
    # RAISE ERROR IF CHAT TYPE IS PRIVATE
    if event.is_private:
        raise TypeError("There is no permission in private chat")

    # Declare some needed variables
    chat = chat if chat else (await event.get_chat())
    user = user if user else (await event.get_sender())
    # permissions lists. All default None. Will be declared after parsing participant info
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
        get_participant_result: types.channels.ChannelParticipant = await event.client(functions.channels.GetParticipantRequest(
            channel = chat,
            participant = user
        ))
        participant = get_participant_result.participant
    except errors.UserNotParticipantError:
        user_perm = chat.default_banned_rights
        participant = member
    if isinstance(participant, admins):
        user_perm = participant.admin_rights
        permissions['change_info'] = user_perm.change_info
        permissions['post_messages'] = user_perm.post_messages
        permissions['edit_messages'] = user_perm.edit_messages
        permissions['delete_messages'] = user_perm.delete_messages
        permissions['ban_users'] = user_perm.ban_users
        permissions['invite_users'] = user_perm.invite_users
        permissions['pin_messages'] = user_perm.pin_messages
        permissions['add_admins'] = user_perm.add_admins
        permissions['anonymous'] = user_perm.anonymous
        permissions['manage_call'] = user_perm.manage_call
        permissions['other'] = user_perm.other
        permissions['view_messages'] = True
        permissions['send_games'] = True
        permissions['send_gifs'] = True
        permissions['send_inline'] = True
        permissions['send_media'] = True
        permissions['send_polls'] = True
        permissions['send_stickers'] = True
        permissions['send_messages'] = True
        permissions['embed_links'] = True
    elif isinstance(participant, (banned, member)):
        if isinstance(participant, banned):
            user_perm = participant.banned_rights
        else:
            user_perm = chat.default_banned_rights
        permissions['view_maaages'] = user_perm.view_messages
        permissions['send_games'] = user_perm.send_games
        permissions['send_gifs'] = user_perm.send_gifs
        permissions['send_inline'] = user_perm.send_inline
        permissions['send_media'] = user_perm.send_media
        permissions['send_polls'] = user_perm.send_polls
        permissions['send_stickers'] = user_perm.send_stickers
        permissions['send_messages'] = user_perm.send_messages
        permissions['embed_links'] = user_perm.embed_links
        permissions['change_info'] = user_perm.change_info
        permissions['invite_users'] = user_perm.invite_users
        permissions['pin_messages'] = user_perm.pin_messages
    
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
        user = await event.get_sender() if user is None else user
        if isinstance(user, patched.User):
            # Sender is user, check member or admin or owner
            try:
                get_participant_result: types.channels.ChannelParticipant = await event.client(functions.channels.GetParticipantRequest(
                    channel = chat,
                    participant = user
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
            if user.megagroup == True:
                return "anonym"
            full: types.messages.ChatFull = await event.client(functions.channels.GetFullChannelRequest(
                channel = await event.get_input_chat()
            ))
            linked_chat_id = full.full_chat.linked_chat_id
            user_id = user.id
            if user_id == linked_chat_id:
                return "channel"
            else:
                return "anonch"

async def get_user(event: Message, user: str|int):
    full_user: types.UserFull =  await event.client(functions.users.GetFullUserRequest(
        id = user
    ))
    return full_user.users[0]

async def send_sticker(client: TelegramClient, peer: types.TypeInputPeer, sticker_id: int, access_hash: int, file_reference: bytes, messages: str = None, silent: bool|None = None):
    """My helper to simplify send sticker process :)"""
    return await client(functions.messages.SendMediaRequest(
        peer = peer,
        media = types.InputMediaDocument(
            id = types.InputDocument(
                id = sticker_id,
                access_hash = access_hash,
                file_reference = file_reference
            )
        ),
        message = messages,
        silent = silent
    ))

# ---------- End async functions ----------
# ---------- Sync functions ----------

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
            tmp = text.find(var[j])
            if j != 0:
                add, subtract = 0, 0
                for k in range(j):
                    add += get_length(str(res[k]))
                    subtract += len(var[k])
                tmp += add - subtract
            offsets.append(tmp)
        
        return offsets, lengths
    else:
        return None

# ---------- End sync functions ----------