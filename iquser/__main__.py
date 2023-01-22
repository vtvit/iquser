import sys
import iquser
from iquser import BOTLOG_CHATID, HEROKU_APP, PM_LOGGER_GROUP_ID
from .Config import Config
from .core.logger import logging
from .core.session import iqub
from .utils import (
    add_bot_to_logger_group,
    install_externalrepo,
    ipchange,
    load_plugins,
    setup_bot,
    mybot,
    startupmessage,
    verifyLoggerGroup,
    saves,
)

LOGS = logging.getLogger("iquser")

print(iquser.__copyright__)
print("Licensed under the terms of the " + iquser.__license__)

cmdhr = Config.COMMAND_HAND_LER

try:
    LOGS.info("دەستی کرد بە دامەزراندن  ✓")
    iqub.loop.run_until_complete(setup_bot())
    LOGS.info("دامەزراندنی بۆت تەواو بوو ✓")
except Exception as e:
    LOGS.error(f"{str(e)}")
    sys.exit()

try:
    LOGS.info("دۆخی سەرهێڵ کاردەکات ..")
    iqub.loop.run_until_complete(mybot())
    LOGS.info("دۆخی سەرهێڵ بە سەرکەوتوویی کاردەکات ✓")
except Exception as iq:
    LOGS.error(f"- {iq}")
    sys.exit()    


class CatCheck:
    def __init__(self):
        self.sucess = True


Catcheck = CatCheck()


async def startup_process():
    check = await ipchange()
    if check is not None:
        Catcheck.sucess = False
        return
    await verifyLoggerGroup()
    await load_plugins("plugins")
    await load_plugins("assistant")
    print("➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖")
    print("᯽︙بۆتی زیرەك کاردەکات بە سەرکەوتوویی ")
    print(
        f"کارکردنی ئۆتۆماتیکی دۆخی سەرهێڵ بنێرە {cmdhr}فەرمانەکان بۆ بینینی فەرمانی سەرچاوە\
        \nبۆ یارمەتیدان بنێرە  https://t.me/VTVIT"
    )
    print("➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖")
    await verifyLoggerGroup()
    await saves()
    await add_bot_to_logger_group(BOTLOG_CHATID)
    if PM_LOGGER_GROUP_ID != -100:
        await add_bot_to_logger_group(PM_LOGGER_GROUP_ID)
    await startupmessage()
    Catcheck.sucess = True
    return

async def externalrepo():
    if Config.VCMODE:
        await install_externalrepo("https://github.com/vtvit/iqmusic", "iqmusic", "iquservc")

iqub.loop.run_until_complete(externalrepo())
iqub.loop.run_until_complete(startup_process())

if len(sys.argv) not in (1, 3, 4):
    iqub.disconnect()
elif not Catcheck.sucess:
    if HEROKU_APP is not None:
        HEROKU_APP.restart()
else:
    try:
        iqub.run_until_disconnected()
    except ConnectionError:
        pass
