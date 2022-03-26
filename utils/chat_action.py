import time
from types import NoneType
from telethon import TelegramClient
from telethon.sync import events
from telethon.tl.types import (
    MessageActionChatAddUser,
    MessageActionChatCreate,
    MessageActionChatDeletePhoto,
    MessageActionChatDeleteUser,
    MessageActionChatJoinedByRequest,
    MessageActionChatEditPhoto,
    MessageActionChatEditTitle,
    MessageActionChatJoinedByLink,
    UpdateBotChatInviteRequester,
    MessageService
)

async def chat_action(event: events.ChatAction.Event):
    """
    Chat Action handler
    """
    client: TelegramClient = event._client
    action = event.action_message
    update = event.original_update

    if isinstance(action, NoneType) and isinstance(update, UpdateBotChatInviteRequester):
        user = await client.get_entity(update.user_id)
        first_name = user.first_name
        last_name = user.last_name
        full_name = first_name + f" {last_name}" if last_name else first_name
        user_id = user.id
        access_hash = user.access_hash
    elif action == None:
        print(event)
    elif isinstance(action.action, MessageActionChatAddUser):
        users = (await client.get_entity(user) for user in action.action.users)
        first_name = (user.first_name for user in users)
        last_name = (user.last_name for user in users)
        user_id = (user.id for user in users)
        access_hash = (user.access_hash for user in users)
        full_name = first_name + f" {last_name}" if last_name else first_name
    elif isinstance(action.action, MessageActionChatJoinedByLink):
        user = await client.get_entity(action.from_id.user_id)
        first_name = user.first_name
        last_name = user.last_name
        full_name = first_name + f" {last_name}" if last_name else first_name
        user_id = user.id
        access_hash = user.access_hash
    
    print(first_name)
    print(last_name)
    print(user_id)
    print(access_hash)
    print(full_name)
    await event.respond(f"Hello [{full_name}](tg://user?id={user_id}), welcome to my chat!")