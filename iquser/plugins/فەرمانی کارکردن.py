import sys
from asyncio.exceptions import CancelledError
from time import sleep
import asyncio
from iquser import iqub

from ..core.logger import logging
from ..core.managers import edit_or_reply
from ..sql_helper.global_collection import (
    add_to_collectionlist,
    del_keyword_collectionlist,
    get_collectionlist_items,
)
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
from . import BOTLOG, BOTLOG_CHATID, HEROKU_APP

LOGS = logging.getLogger(__name__)
plugin_category = "tools"


@iqub.iq_cmd(
    pattern="دەستپێکردنەوە$",
    command=("دەستپێکردنەوە", plugin_category),
    info={
        "header": "Restarts the bot !!",
        "usage": "{tr}restart",
    },
    disable_errors=True,
)
async def _(event):
    "Restarts the bot !!"
    if BOTLOG:
        await event.client.send_message(BOTLOG_CHATID, "**⌔︙بـۆتـی زیـرەك ↻** \n" "**᯽︙ بە سەرکەوتوویی دەستیپێکردەوە ✅ ↻**")
    VTVIT = await edit_or_reply(event, "᯽︙ دەست دەکاتەوە بە کارکردن کەمێك چاوەڕێ بکە ")
    await event.edit("0%\n▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒")
    await asyncio.sleep(2)
    await event.edit("4%\n█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒")
    await asyncio.sleep(2)
    await event.edit("8%\n██▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒")
    await asyncio.sleep(2)
    await event.edit("20%\n█████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒")
    await asyncio.sleep(2)
    await event.edit("36%\n█████████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒")
    await asyncio.sleep(2)
    await event.edit("52%\n█████████████▒▒▒▒▒▒▒▒▒▒▒▒")
    await asyncio.sleep(2)
    await event.edit("84%\n█████████████████████▒▒▒▒")
    await asyncio.sleep(2)
    await event.edit("100%\n████████████████████████")
    await asyncio.sleep(2)
    await event.edit("**᯽︙ بە سەرکەوتوویی دەستپێدەکاتەوە لە ماوەی ✓ \nچاوەڕێ بکە 2-5 خولەك**")
    await asyncio.sleep(2)
    try:
        ulist = get_collectionlist_items()
        for i in ulist:
            if i == "restart_update":
                del_keyword_collectionlist("restart_update")
    except Exception as e:
        LOGS.error(e)
    try:
        add_to_collectionlist("restart_update", [VTVIT.chat_id, VTVIT.id])
    except Exception as e:
        LOGS.error(e)
    try:
        delgvar("ipaddress")
        await iqub.disconnect()
    except CancelledError:
        pass
    except Exception as e:
        LOGS.error(e)


@iqub.iq_cmd(
    pattern="کوژاندنەوە$",
    command=("کوژاندنەوە", plugin_category),
    info={
        "header": "کوژاندنەوەی بۆت !!",
        "description": "To turn off the dyno of heroku. you cant turn on by bot you need to got to heroku and turn on or use @hk_heroku_bot",
        "usage": "{tr}کوژاندنەوە",
    },
)
async def _(event):
    "Shutdowns the bot"
    if BOTLOG:
        await event.client.send_message(BOTLOG_CHATID, "**᯽︙ وەستاندنی کارکردن ✕ **\n" "**᯽︙ تـمبە سەرکەوتوویی بۆت لە کارکردن وەستا ✓**")
    await edit_or_reply(event, "**᯽︙ بۆت دەوەستێ ئێستا ..**\n᯽︙  **بە دەستی من دەستپێبکەوە دواتر لە ڕێگەی دامەزرێنەرەکان ..**\n⌔︙**بۆت وەستێنرا لە کارکردن **")
    if HEROKU_APP is not None:
        HEROKU_APP.process_formation()["worker"].scale(0)
    else:
        sys.exit(0)

@iqub.iq_cmd(
    pattern="نوێکردنەوەکان (چالاک|ناچالاک)$",
    command=("نوێکردنەوەکان", plugin_category),
    info={
        "header": "᯽︙ بۆ نوێکردنەوەی دوای دەستپێکردنەوە و داگرتن  ",
        "description": "⌔︙دواتر بنێرە پینگ cmds وەڵامدانەوەی لە دوایین نامەی پێشوو (دەستپێکردنەوە/داگرتنەوە /نوێکردنەوە cmds) 💡.",
        "usage": [
            "{tr}نوێکردنەوەکان <چالاك/ناچالاك",
        ],
    },
)
async def set_pmlog(event):
    "᯽︙ بۆ نوێکردنەوەی چات لە دوای دەستپێکردنەوە یان داگرتنەوە  "
    input_str = event.pattern_match.group(1)
    if input_str == "ناچالاك":
        if gvarstatus("restartupdate") is None:
            return await edit_delete(event, "**᯽︙ نوێکردنەوەکان پێشتر ناچالاكکراون ❗️**")
        delgvar("restartupdate")
        return await edit_or_reply(event, "**⌔︙نوێکردنەوەکان بەسەرکەوتوویی ناچالاكکران ✓**")
    if gvarstatus("restartupdate") is None:
        addgvar("restartupdate", "turn-oned")
        return await edit_or_reply(event, "**⌔︙بە سەرکەوتوویی نوێکردنەوەکان چالاککران ✓**")
    await edit_delete(event, "**᯽︙ نوێکردنەوەکان پێشتر چالاککراون ❗️**")
