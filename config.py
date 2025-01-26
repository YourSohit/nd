import os
from dotenv import load_dotenv
load_dotenv()

def is_enabled(value, default):
    if value.lower() in ["true", "yes", "1", "enable", "y"]:
        return True
    elif value.lower() in ["false", "no", "0", "disable", "n"]:
        return False
    else:
        return default

# Mandatory variables for the bot to start
API_ID = int(os.environ.get("API_ID", "977080"))
API_HASH = os.environ.get("API_HASH", "0c20c4265501492a1513f91755acd42b")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "YOUR_BOT_TOKEN")
OWNER_ID = int(os.environ.get("OWNER_ID", "399726799"))
DATABASE_URL = os.environ.get("DATABASE_URL", "mongodb+srv://abcd:abcd@cluster0.cii4jll.mongodb.net/?retryWrites=true&w=majority")
DATABASE_NAME = os.environ.get("DATABASE_NAME", "WebNotificationBot")
LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "-1001363692085"))
BOT_USERNAME = os.environ.get("BOT_USERNAME", "serials_notify_bot")
BROADCAST_AS_COPY = is_enabled(os.environ.get("BROADCAST_AS_COPY", "True"), True)

VALIDITY = [int(i.strip()) for i in os.environ.get("VALIDITY", "7,30,90,180,365").split(",")] 

TRANSLATION_LANG = """Kannada,kn
English,en
Hindi,hi
Bengali,bn
Tamil,ta
Telugu,te"""

languages = os.environ.get("TRANSLATION_LANG", TRANSLATION_LANG).replace(r'\n', '\n').split("\n")

IS_USER_ALLOWED_TO_CHANGE_LANGUAGE = is_enabled(os.environ.get("IS_USER_ALLOWED_TO_CHANGE_LANGUAGE", "True"), True)

# Replit Config
REPLIT_USERNAME = os.environ.get("REPLIT_USERNAME", None)
REPLIT_APP_NAME = os.environ.get("REPLIT_APP_NAME", None)
REPLIT = f"https://{REPLIT_APP_NAME.lower()}.{REPLIT_USERNAME}.repl.co" if REPLIT_APP_NAME and REPLIT_USERNAME else False
PING_INTERVAL = int(os.environ.get("PING_INTERVAL", "300"))

# API Endpoints for OTTs
ZEE5_API_URL = "https://gwapi.zee5.com/content/tvshow/{show_id}?translation=en&country=IN"
HOTSTAR_API_URL = "https://api.hotstar.com/o/v1/show/detail?contentId={show_id}"
SUNNXT_API = "https://pwaapi.sunnxt.com/content/v2/carousel/portalTvshowsLatestEpisodes?&level=devicemax&startIndex=1&count=10"
JIOCINEMA_API_URL = "https://www.jiocinema.com/api/show/{show_id}"
DANGALPLAY_API_URL = "https://www.dangalplay.com/api/show/{show_id}"
SONYLIV_API_URL = "https://www.sonyliv.com/api/show/{show_id}"
ETVWIN_API_URL = "https://www.etvwin.com/api/show/{show_id}"
