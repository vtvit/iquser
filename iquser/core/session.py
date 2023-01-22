import sys
from iquser.core.logger import logging
from telethon.network.connection.tcpabridged import ConnectionTcpAbridged
from telethon.sessions import StringSession
from telethon.errors import AccessTokenExpiredError, AccessTokenInvalidError
from ..Config import Config
from .client import IQUserBotClient
LOGS = logging.getLogger(" ")

__version__ = "2.10.6"

loop = None

if Config.STRING_SESSION:
    session = StringSession(str(Config.STRING_SESSION))
else:
    session = "iquser"

try:
    iqub = IQUserBotClient(
        session=session,
        api_id=Config.APP_ID,
        api_hash=Config.API_HASH,
        loop=loop,
        app_version=__version__,
        connection=ConnectionTcpAbridged,
        auto_reconnect=True,
        connection_retries=None,
    )
except Exception as e:
    print(f"[STRING SESSION] - {str(e)}")
    sys.exit()

try:
    iqub.tgbot = tgbot = IQUserBotClient(
        session="iqTgbot",
        api_id=Config.APP_ID,
        api_hash=Config.API_HASH,
        loop=loop,
        app_version=__version__,
        connection=ConnectionTcpAbridged,
        auto_reconnect=True,
        connection_retries=None,
    ).start(bot_token=Config.TG_BOT_TOKEN)
except AccessTokenExpiredError:
    LOGS.error("ئەگەر تۆکنی بۆت بەسەرچووە، بیگۆڕە بۆ ئەوەی سەرچاوە کار بکات")
except AccessTokenInvalidError:
    LOGS.error("تۆکنی بۆتەکە نادروستە، بیگۆڕە بۆ ئەوەی سەرچاوەکە کاربکا")
