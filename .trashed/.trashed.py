async def get_perm(event: Message, chat: types.TypeInputChannel = None, user: types.TypeInputPeer = None, status: str = None):
    chat = await event.get_chat() if chat is None else chat
    user = await event.get_sender() if user is None else user
    status = await check_status(event, chat, user) if status is None else status
    if status in ['channel', 'anonch', 'anonym', 'private']:
        return None

    participant: types.channels.ChannelParticipant = await event.client(functions.channels.GetParticipantRequest(
        channel = chat,
        participant = user
    ))

    if status in ['admin', 'creator']:
        return participant.participant.admin_rights
    elif status == "member":
        chat: types.Channel = await event.get_chat()
        return chat.default_banned_rights
    elif status == "restricted":
        return participant.participant.banned_rights
    else:
        return None