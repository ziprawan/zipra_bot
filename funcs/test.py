from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
import os

async def main(msg: Message, cmd, args):
    # Gather all information of members on chat
    if msg.chat.type == 'private':
        return await msg.reply("Kau mau cek list bot di private dan itu bukanlah ide yg bagus")
    list_of_users = []

    # Filtering for bot only
    async for i in msg.chat.iter_members():
        # Append username
        list_of_users.append(i.user)
    
    # Collecting data for message text
    amount_of_members = len(list_of_users)
    message = f"Jumlah member di grup {msg.chat.title} sebanyak {amount_of_members}. Diantaranya:\n\n"
    for i in range(0, amount_of_members):
        if list_of_users[i].is_deleted:
            continue
        else:
            message += f"{i + 1}. [{list_of_users[i].first_name}](tg://user?id={list_of_users[i].id})\n"
    
    # Check length of message
    if len(message) > 4096:
        with open("members.txt", "w") as file:
            file.write(message)
        await msg.reply_document('members.txt')

        # Clean file
        if os.path.exists("members.txt"):
            os.remove("members.txt")
        return True
    else:
        # Send Result
        return await msg.reply(message)