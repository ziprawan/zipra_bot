from pyrogram.types import Message

async def main(msg: Message, *another):
    if msg.chat.type == 'private':
        return await msg.reply("Kau mau cek list bot di private dan itu bukanlah ide yg bagus")
    list_of_bots = []

    # Filtering for bot only
    async for i in msg.chat.iter_members(filter="bots"):
        # Append username
        list_of_bots.append(f'@{i.user.username}')
    
    # Collecting data for message text
    amount_of_bots = len(list_of_bots)
    message = f"Jumlah bot di grup {msg.chat.title} sebanyak {amount_of_bots}. Diantaranya:\n\n"
    for i in range(0, amount_of_bots):
        message += f"{i + 1}. {list_of_bots[i]}\n"
    
    # Send Result
    await msg.reply(message)