import sys
import iquser
from iquser import BOTLOG_CHATID, HEROKU_APP, PM_LOGGER_GROUP_ID
from .Config import Config
from .core.logger import logging
from .core.session import jepiq
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
    LOGS.info("دەست پێکردنی بۆتی زیرەك ✓")
    iquser.loop.run_until_complete(setup_bot())
    LOGS.info("دەمەزراندنەکە تەواو بوو ✓")
except Exception as e:
    LOGS.error(f"{str(e)}")
    sys.exit()

try:
    LOGS.info("دۆخی سەرهێڵ چالاککراوە")
    iquser.loop.run_until_complete(mybot())
    LOGS.info("دۆخی سەرهێڵ بە سەرکەوتوویی چالاککرا ✓")
except Exception as IQ:
    LOGS.error(f"- {IQ}")
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
    print("᯽︙بۆتی زیرەك بە سەرکەوتوویی کاردەکات ")
    print(
        f" پێکردنی سەرهێڵ بە خودکار بنێرە {cmdhr}فەرمانەکان بۆ بینینی فەرمانی سەرچاوە\
        \nیارمەتیدان  https://t.me/VTVIT"
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
        await install_externalrepo("https://github.com/vtvit/iqmusic", "iqmusic", "iqmusicvc")

iquser.loop.run_until_complete(externalrepo())
iquser.loop.run_until_complete(startup_process())

if len(sys.argv) not in (1, 3, 4):
    iquser.disconnect()
elif not Catcheck.sucess:
    if HEROKU_APP is not None:
        HEROKU_APP.restart()
else:
    try:
        jepiq.run_until_disconnected()
    except ConnectionError:
        pass
