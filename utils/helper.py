import struct

def add_surrogate(text):
    """Adding surrogate to the text.
    SMP -> Surrogate Pairs (Telegram offsets are calculated with these).
    See https://en.wikipedia.org/wiki/Plane_(Unicode)#Overview for more.
    
    Big thanks to telethon dev!"""
    return "".join(
        "".join(
            chr(y) for y in struct.unpack("<HH", x.encode("utf-16le"))
        ) if (0x10000 <= ord(x) <= 0x10FFFF)
        else x
        for x in text
    )

def get_length(text):
    return len(add_surrogate(text))