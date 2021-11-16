from pyrogram.types import Message

def main(msg: Message):
    """Untuk mengecek apakah user di grup itu termasuk administrator/anonymous/creator"""
    if msg.sender_chat != None and msg.sender_chat.type != 'channel': 
        # Anonymous dan channel tidak punya akses
        return 'anonymous'
    elif msg.sender_chat != None and msg.sender_chat.type == 'channel':
        return False
    else:
        # Else
        result = msg.chat.get_member(msg.from_user.id)
        if result.status == 'administrator':
            return 'administrator'
        elif result.status == 'creator':
            return 'creator'
        else:
            return False
