import json
import os
import re

from telethon.events import CallbackQuery

from iquser import iqub


@iqub.tgbot.on(CallbackQuery(data=re.compile(b"secret_(.*)")))
async def on_plug_in_callback_query_handler(event):
    timestamp = int(event.pattern_match.group(1).decode("UTF-8"))
    if os.path.exists("./iquser/secret.txt"):
        jsondata = json.load(open("./iquser/secret.txt"))
        try:
            message = jsondata[f"{timestamp}"]
            userid = message["userid"]
            ids = userid + [iqub.uid]
            if event.query.user_id in ids:
                encrypted_tcxt = message["text"]
                reply_pop_up_alert = encrypted_tcxt
            else:
                reply_pop_up_alert = "بۆچی سەیری ئەم گێلانە دەکەیت و کاری خۆت دەکەیت، گەمژە👾."
        except KeyError:
            reply_pop_up_alert = "ئەم نامەیە چیتر لە سێرڤەری بۆتی زیرەك بوونی نییە👾"
    else:
        reply_pop_up_alert = "ئەم نامەیە چی تر بوونی نییە 👾"
    await event.answer(reply_pop_up_alert, cache_time=0, alert=True)
