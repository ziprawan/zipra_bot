from telethon.sync import events
from telethon.tl.types import (
    MessageActionChatAddUser,
    MessageActionChatCreate,
    MessageActionChatDeletePhoto,
    MessageActionChatDeleteUser,
    MessageActionChatJoinedByRequest,
    MessageActionChatEditPhoto,
    MessageActionChatEditTitle,
    MessageActionChatJoinedByLink
)

async def chat_action(event: events.ChatAction.Event):
    msg = event.action_message
    if isinstance(msg.action, MessageActionChatAddUser):
        joined_users = msg.action.users
        added_by = msg.from_id.user_id
        me = await event.client.get_me()
        if me.id in joined_users:
            return await event.respond("Hemlo")
        else:
            return await event.respond(f"Hi {joined_users}. Added by: {added_by}")