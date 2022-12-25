import json
import os
import re

from telethon.events import CallbackQuery

from iquser import iqub


@iqub.tgbot.on(CallbackQuery(data=re.compile(b"hide_(.*)")))
async def on_plug_in_callback_query_handler(event):
    timestamp = int(event.pattern_match.group(1).decode("UTF-8"))
    if os.path.exists("./iquser/hide.txt"):
        jsondata = json.load(open("./iquser/hide.txt"))
        try:
            reply_pop_up_alert = jsondata[f"{timestamp}"]["text"]
        except KeyError:
            reply_pop_up_alert = "- ببوورە .. ئەم نامەیە چیتر لە سێرڤەری بۆتی زیرەك نییە"
    else:
        reply_pop_up_alert = "- ببوورە .. ئەم نامەیە چیتر لە سێرڤەری بۆتی زیرەك نییە"
    await event.answer(reply_pop_up_alert, cache_time=0, alert=True)
