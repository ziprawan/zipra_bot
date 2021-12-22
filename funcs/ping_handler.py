import time, pyrogram.emoji as emoji

async def main(msg, *another):
    result = await msg.reply(f"{emoji.PING_PONG} **PONG!!!**")
    first_time = msg.edit_date if msg.edit_date else msg.date
    last_time = time.time()
    response_time = round(last_time - first_time, 3)
    return await result.edit(f"**{result.text}**\n⏱ <code>{response_time}'s</code>")
