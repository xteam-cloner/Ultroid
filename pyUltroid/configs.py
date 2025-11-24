import sys

from decouple import config

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


class Var:
    if len(sys.argv) > 1:
        API_ID = int(sys.argv[1])
    else:
        API_ID = config("API_ID", cast=int)
        
    if len(sys.argv) > 2:
        API_HASH = sys.argv[2]
    else:
        API_HASH = config("API_HASH")
        
    if len(sys.argv) > 3:
        SESSION = sys.argv[3]
    else:
        SESSION = config("SESSION")
        
    API_ID2 = config("API_ID2", cast=int, default=None) 
    API_HASH2 = config("API_HASH2", default=None) 
    SESSION2 = config("SESSION2", default=None)
    
    API_ID3 = config("API_ID3", cast=int, default=None)
    API_HASH3 = config("API_HASH3", default=None)
    SESSION3 = config("SESSION3", default=None)
    
    REDIS_URI = (
        sys.argv[4]
        if len(sys.argv) > 4
        else (config("REDIS_URI", default=None) or config("REDIS_URL", default=None))
    )
    REDIS_PASSWORD = (
        sys.argv[5] if len(sys.argv) > 5 else config("REDIS_PASSWORD", default=None)
    )
    # extras
    BOT_TOKEN = config("BOT_TOKEN", default=None)
    LOG_CHANNEL = config("LOG_CHANNEL", default=0, cast=int)
    HEROKU_APP_NAME = config("HEROKU_APP_NAME", default=None)
    HEROKU_API = config("HEROKU_API", default=None)
    VC_SESSION = config("VC_SESSION", default=None)
    ADDONS = config("ADDONS", default=False, cast=bool)
    VCBOT = config("VCBOT", default=False, cast=bool)
    # for railway
    REDISPASSWORD = config("REDISPASSWORD", default=None)
    REDISHOST = config("REDISHOST", default=None)
    REDISPORT = config("REDISPORT", default=None)
    REDISUSER = config("REDISUSER", default=None)
    # for sql
    DATABASE_URL = config("DATABASE_URL", default=None)
    # for MONGODB users
    MONGO_URI = config("MONGO_URI", default=None)
