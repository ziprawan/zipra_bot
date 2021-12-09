import time

async def main(msg, *another):
    result = await msg.reply("🏓 **PONG!!!**")
    first_time = msg.date
    last_time = time.time()
    response_time = round(last_time - first_time, 3)
    return await result.edit(f"**{result.text}**\n⏱ <code>{response_time}'s</code>")
