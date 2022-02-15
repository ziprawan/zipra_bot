import sys, io, traceback

from telethon.tl.custom.message import Message
from utils.helper import get_length
from utils.init import owner

async def main(*args):
    event: Message = args[0]
    parser = args[1]

    code = await parser.get_options()

    if (await event.get_reply_message()) != None:
        msg = await event.get_reply_message()
    else:
        msg = event


    if (await event.get_sender()).id != owner:
        return None
    elif code == None:
        return await event.respond("No code...")

    old_stderr = sys.stderr
    old_stdout = sys.stdout
    re_out = sys.stdout = io.StringIO()
    re_err = sys.stderr = io.StringIO()
    stdout, stderr, exc = None, None, None

    try:
        await aexec(code, event, event.client)
    except:
        exc = traceback.format_exc()

    stdout = re_out.getvalue()
    stderr = re_err.getvalue()
    sys.stderr = old_stderr
    sys.stdout = old_stdout

    result = None
    if exc:
        result = exc
    elif stderr:
        result = stderr
    elif stdout:
        result = stdout
    
    if result != None:
        if get_length(result) > 4096:
            with io.BytesIO(str.encode(result)) as out:
                out.name = "eval.txt"
                return await event.respond(file=out)
        else:
            return await event.respond(result)

async def aexec(code: str, event, client):
    exec(
        "async def __aexec(event, client): "
        + "".join(f"\n {c}" for c in code.split("\n"))
    )
    return await locals()['__aexec'](event, client)