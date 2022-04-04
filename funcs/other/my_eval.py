import sys, io, traceback, logging
from telethon.tl.custom.message import Message
from telethon.tl.types import MessageEntityCode
from utils.helper import get_length, send_sticker
from utils.init import owner
from utils.lang import Language

async def main(*args):
    logging.debug("[EvalHandler] Setting up variables")
    event: Message = args[0]
    parser = args[1]
    lang = Language(event)

    code = parser.get_args()[1]

    if (await event.get_sender()).id != owner:
        logging.info("[EvalHandler] The sender is my owner. Aborting")
        return
    elif code == None:
        logging.debug("[EvalHandler] Code not found. Aborting")
        return await event.respond(await lang.get('no_code'))

    old_stderr = sys.stderr
    old_stdout = sys.stdout
    re_out = sys.stdout = io.StringIO()
    re_err = sys.stderr = io.StringIO()
    stdout, stderr, exc = None, None, None

    logging.debug("[EvalHandler] Executing code")
    try:
        await aexec(code, event, event.client)
    except:
        exc = traceback.format_exc()

    logging.debug("[EvalHandler] Parsing output")
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
        result = result.strip()
        if result == "":
            return True
        if get_length(result) > 4096:
            logging.debug(f"[EvalHandler] Message length is {get_length(result)}. Sending as file instead.")
            with io.BytesIO(str.encode(result)) as out:
                out.name = "eval.txt"
                return await event.respond(file=out)
        else:
            logging.debug("[EvalHandler] Message length is less than 4096. Sending as message")
            return await event.respond(
                result, 
                parse_mode=None,
                formatting_entities = [MessageEntityCode(
                    offset = 0,
                    length = get_length(result)
                )])

async def aexec(code: str, event, client):
    exec(
        "async def __aexec(event, client): "
        + "".join(f"\n {c}" for c in code.split("\n"))
    )
    return await locals()['__aexec'](event, client)