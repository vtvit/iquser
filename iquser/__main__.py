import contextlib
import sys

import iquser
from iquser import BOTLOG_CHATID, PM_LOGGER_GROUP_ID

from .Config import Config
from .core.logger import logging
from .core.session import iqub
from .utils import mybot
from .utils import (
    add_bot_to_logger_group,
    install_externalrepo,
    load_plugins,
    setup_bot,
    startupmessage,
    verifyLoggerGroup,
)


LOGS = logging.getLogger("iquser")
cmdhr = Config.COMMAND_HAND_LER

print(iquser.__copyright__)
print(f"مۆڵەتی پێدراوە لەژێر مەرجەکانی  {iquser.__license__}")

cmdhr = Config.COMMAND_HAND_LER

try:
    LOGS.info("⌭ دەست بکە بە دابەزاندنی بۆتی زیرەك ⌭")
    iqub.loop.run_until_complete(setup_bot())
    LOGS.info("⌭ دەست بکە بە کارکردنی بۆت👾 ⌭")
except Exception as e:
    LOGS.error(f"{e}")
    sys.exit()


try:
    LOGS.info("⌭ دۆخی سەرهێڵ چالاککراوە👾 ⌭")
    iqub.loop.run_until_complete(mybot())
    LOGS.info("✓ بە سەرکەوتوویی دۆخی سەرهێڵ چالاکرا👾 ✓")
except Exception as e:
    LOGS.error(f"- {e}")


try:
    LOGS.info("⌭ ئێکسسواراتەکان دادەبەزن .. 👾⌭")
    iqub.loop.create_task(saves())
    LOGS.info("✓ بە سەرکەوتوویی .. دابەزێنرا ✓")
except Exception as e:
    LOGS.error(f"- {e}")


async def startup_process():
    await verifyLoggerGroup()
    await load_plugins("plugins")
    await load_plugins("assistant")
    LOGS.info(f"⌔┊بە سەرکەوتوویی بۆتی زیرەك .. دامەزرا 👾 ✓")
    await verifyLoggerGroup()
    await add_bot_to_logger_group(BOTLOG_CHATID)
    if PM_LOGGER_GROUP_ID != -100:
        await add_bot_to_logger_group(PM_LOGGER_GROUP_ID)
    await startupmessage()
    return


iqub.loop.run_until_complete(startup_process())

if len(sys.argv) in {1, 3, 4}:
    with contextlib.suppress(ConnectionError):
        iqub.run_until_disconnected()
else:
    iqub.disconnect()
