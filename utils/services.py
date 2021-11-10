from utils.service_database import get_data

def main(msg):
    group = msg.chat.id
    if msg.chat.type == "private":
        return
    result = get_data(group)
    if result == None or result == False:
        return
    elif result == True:
        try:
            msg.delete()
        except:
            pass