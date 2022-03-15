import logging
from telethon import _ as patched, functions, types, TelegramClient

async def main(*args):
    logging.debug("[ScopeHandler] Setting up variables")
    event: patched.Message = args[0]
    client: TelegramClient = event.client
    replied: patched.Message = await event.get_reply_message()
    if replied == None:
        logging.debug("[ScopeHandler] No reply. Aborting")
        return await event.reply("No reply detected")
    
    sender: patched.User = await replied.get_sender()
    if isinstance(sender, types.Channel):
        logging.debug("[ScopeHandler] Channel detected. No scope for channel. Aborting")
        return await event.reply("Channel doesn't have command scope")
    if sender.bot != True:
        logging.debug("[ScopeHandler] User is not a bot. Aborting")
        return await event.reply("Reply to bot only")

    logging.debug("[ScopeHandler] Getting full chat info")
    input_channel = await event.get_input_chat()

    get_full_chat_request_result: types.messages.ChatFull = await client(functions.channels.GetFullChannelRequest(
        channel = input_channel
    ))
    bot_infos = get_full_chat_request_result.full_chat.bot_info
    for bot_info in bot_infos:
        if bot_info.user_id == sender.id:
            logging.debug(f"[ScopeHandler] Found bot scope for {sender.first_name} [{sender.id}]")
            commands = bot_info.commands
            logging.debug("[ScopeHandler] Creating message")
            if len(commands) == 0:
                message_text = f"Bot {sender.first_name} doesn't have scope command"
            else:
                message_text = f"Bot {sender.first_name} has {len(commands)} command scope(s).\n\n"
                for command in commands:
                    message_text += f"/{command.command} - {command.description}\n"
                
            logging.debug("[ScopeHandler] Sending message")
            return await event.reply(message_text)