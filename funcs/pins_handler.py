from pyrogram.types import Message
from pyrogram import raw

async def unpin_all(msg: Message) -> bool:
    result = await msg._client.unpin_all_chat_messages(msg.chat.id)
    await msg.reply("Semua pesan yg di pin berhasil di unpin!")
    return result

async def unpin_msg(msg: Message) -> bool:
    chat = await msg._client.get_chat(msg.chat.id)
    if msg.reply_to_message != None:
        await msg.reply_to_message.unpin()
        await msg.reply("Berhasil unpin pesan yg kau reply!", True)
        return True
    await msg._client.unpin_chat_message(msg.chat.id, chat.pinned_message.message_id)
    await msg.reply("Unpin pesan berhasil!", True)
    return True

async def pin_msg(msg: Message) -> bool:
    if msg.reply_to_message == None:
        await msg.reply("Balas ke suatu pesan agar ku pin", True)
    else:
        pinned: raw.types.Updates = await msg._client.send(
            raw.functions.messages.UpdatePinnedMessage(
                peer = await msg._client.resolve_peer(
                    msg.chat.id
                ),
                id = msg.reply_to_message.message_id,
                silent = True
            )
        )
        await msg._client.delete_messages(msg.chat.id, pinned.updates[0].id)
        return await msg.reply("Pesan berhasil di pin!", True)

async def pin_loud(msg: Message) -> bool:
    if msg.reply_to_message == None:
        await msg.reply("Balas ke suatu pesan agar ku pin", True)
    else:
        pinned = await msg._client.send(
            raw.functions.messages.UpdatePinnedMessage(
                peer = await msg._client.resolve_peer(
                    msg.chat.id
                ),
                id = msg.reply_to_message.message_id,
                silent = False
            )
        )
        await msg._client.delete_messages(
            chat_id = msg.chat.id,
            message_ids = pinned.updates[0].id
        )
        return await msg.reply("Pesan ini sudah aku pin dan ku kasih tau ke yg lain!", True)

async def main(msg: Message, cmd: str, args: str) -> bool:
    # Jika bukan anonymous 
    if msg.sender_chat != None:
        if msg.sender_chat.type == "channel":
            return await msg.reply("Oh, you can't to do this 🗿", True)
    else:
        user = await msg.chat.get_member(msg.from_user.id)
        if user.status != "administrator" and user.status != "creator":
            return await msg.reply("Maaf, kamu harus menjadi admin untuk melakukan ini :/", True)
    if cmd == 'pin':
        if args == None:
            await pin_msg(msg)
        elif args == 'loud':
            await pin_loud(msg)
        else:
            await msg.reply("<code>Parameter is invalid!</code>", True)
    elif cmd == 'unpin':
        if args == None:
            await unpin_msg(msg)
        elif args == 'all':
            await unpin_all(msg)
        else:
            await msg.reply("<code>Parameter is invalid!</code>", True)
    else:
        await msg.reply("<code>Something went wrong!</code>", True)