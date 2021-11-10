import os

def main(msg, *another):
    json_file = open('result.txt', 'w')
    json_file.write(str(msg))
    json_file.close()
    msg.reply_document('result.txt', True, caption="Result")
    if os.path.exists('result.txt'):
        os.remove('result.txt')
