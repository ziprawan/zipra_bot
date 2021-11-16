from pyrogram.types import Message

def main(msg: Message):
    """Untuk mengecek apakah user di grup itu termasuk administrator/anonymous/creator"""
    if msg.sender_chat != None and msg.sender_chat.type != 'channel': 
        # Anonymous dan channel tidak punya akses
        print(1)
        return 'anonymous'
    elif msg.sender_chat != None and msg.sender_chat.type == 'channel':
        print(2)
        return False
    else:
        # Else
        result = msg.chat.get_member(msg.from_user.id)
        print(result.status)
        print(3)
        if result.status == 'administrator':
            print(4)
            return 'administrator'
        elif result.status == 'creator':
            print(5)
            return 'creator'
        else:
            print(6)
            return False
