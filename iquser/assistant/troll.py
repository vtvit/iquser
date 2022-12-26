import json
import os
import re

from telethon.events import CallbackQuery

from iquser import iqub


@iqub.tgbot.on(CallbackQuery(data=re.compile(b"troll_(.*)")))
async def on_plug_in_callback_query_handler(event):
    timestamp = int(event.pattern_match.group(1).decode("UTF-8"))
    if os.path.exists("./iquser/troll.txt"):
        jsondata = json.load(open("./iquser/troll.txt"))
        try:
            message = jsondata[f"{timestamp}"]
            userid = message["userid"]
            ids = [userid]
            if event.query.user_id in ids:
                reply_pop_up_alert = (
                    "کەرە ئەم نامەیە بۆتۆ نییە🕷️"
                )
            else:
                encrypted_tcxt = message["text"]
                reply_pop_up_alert = encrypted_tcxt
        except KeyError:
            reply_pop_up_alert = "-ئەم نامەیە چیتر لە سێرڤەری بۆتی زیرەك بوونی نییە👾"
    else:
        reply_pop_up_alert = "-ئەم نامەیە چی تر بوونی نییە 👾"
    await event.answer(reply_pop_up_alert, cache_time=0, alert=True)
