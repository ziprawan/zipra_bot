from utils.service_database import insert_data, get_data

async def main(msg, command, option):
    group = msg.chat.id
    if msg.chat.type == "private":
        return
    if option == "no" or option == "false" or option == "off":
        opt = False
    elif option == "yes" or option == "true" or option == "on":
        opt = True
    elif option == None or option == "":
        p = await get_data(group)
        return await msg.reply(f"Current settings for cleanservice is: {p}")
    else:
        return await msg.reply("Invalid arguments!\n\nArgumen tersedia: \"true/false\", \"yes/no\", dan \"on/off\"")

    result = await insert_data(group, opt)
    if result == True:
        return await msg.reply("Baiklah, setiap ada service message, akan saya hapus!", True)
    elif result == False:
        return await msg.reply("Baiklah, setiap ada service message, tidak akan saya hapus!", True)
    else:
        return await msg.reply("<code>Something went wrong while input to database!</code>", True)