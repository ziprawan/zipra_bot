import struct


def add_surrogate(text):
    """
    Add surrogate pair to a string
    """
    return ''.join(
        ''.join(
            chr(y) for y in struct.unpack("<HH", x.encode("utf-16le"))
        ) if (0x10000 <= ord(x) <= 0x10FFFF)
        else x
        for x in text
    )

def get_length(text):
    """
    Get the length of a string
    """
    return len(add_surrogate(text))