from utils.service_database import get_data

async def main(msg):
    group = msg.chat.id
    if msg.chat.type == "private":
        return
    result = await get_data(group)
    if result == None or result == False:
        return
    elif result == True:
        try:
            await msg.delete()
        except:
            pass