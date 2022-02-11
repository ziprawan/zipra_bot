from funcs import *
from callback import *

commands = {
    'start': start, 'dbg': dbg, 'ping': ping,
    'help': help, 'setlang': lang
}

callbacks = {
    'help': chelp, 'setlang': clang
}