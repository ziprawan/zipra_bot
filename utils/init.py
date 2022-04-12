import dotenv
import logging
import os
import time
from telethon.sync import TelegramClient

# Load .env
if os.path.exists('.env'):
    dotenv.load_dotenv('.env')
else:
    logging.warning("[init] .env file not found. Using defaults.")

env = os.environ
api_id = env.get("API_ID", None)
api_hash = env.get("API_HASH", None)
bot_token = env.get("BOT_TOKEN", None)
owner = int(env.get("OWNER", None))
debug = str(env.get("DEBUG", None)).lower()
start_time = time.time()

if not api_id or not api_hash or not bot_token:
    logging.error("[init] API_ID, API_HASH or BOT_TOKEN not found. Aborting.")
    raise ValueError("Environment is missing!")

try:
    api_id = int(api_id)
except TypeError:
    api_id = 0

if debug in ["true", "yes", "enabled", 'y']:
    debug = True
else:
    debug = False

supported_lang = {
    'id': 'Indonesia',
    'en': 'English',
    'ar': 'Arabic',
    'ja': 'Japan',
    'ms': 'Malay'
}

if bot_token == "" or bot_token is None:
    raise ValueError("Your Bot Token cannot be empty or None.")

# End read .env
# Initialize client
client = TelegramClient("mybot", api_id, api_hash, request_retries=10, connection_retries=10).start(bot_token=bot_token)

with client:
    me = client.get_me()
