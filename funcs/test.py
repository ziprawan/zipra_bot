from pyrogram.types import Message
import asyncio

async def main(msg: Message, cmd, args):
    channel = (await msg._client.get_chat(msg.chat.id)).linked_chat
    try:
        subs = []
        non_subs = []
        async for i in channel.iter_members():
            subs.append(i.user.id)
        async for j in msg.chat.iter_members():
            if j.user.id not in subs:
                non_subs.append(j.user.first_name)
        return await msg.reply(f"Jumlah user yang tidak join channel {channel.title} sebanyak {len(non_subs)} user")
    except:
        return await msg.reply("Saya bukan admin di channel ini!")