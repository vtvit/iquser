# Copyright (C) 2021 IQUSER TEAM
# FILES WRITTEN BY  @VTVIT

import requests
from validators.url import url

from iquser import iqub

from ..core.managers import edit_delete, edit_or_reply

plugin_category = "utils"


@iqub.ar_cmd(
    pattern="dns(?:\s|$)([\s\S]*)",
    command=("dns", plugin_category),
    info={
        "header": "بۆ بەدەست هێنانی سیستەمی ناوی دۆمەین(dns) لە بەستەری دراوە.",
        "usage": "{tr}dns <url/reply to url>",
        "examples": "{tr}dns google.com",
    },
)
async def _(event):
    "To get Domain Name System(dns) of the given link."
    input_str = "".join(event.text.split(maxsplit=1)[1:])
    reply = await event.get_reply_message()
    if not input_str and reply:
        input_str = reply.text
    if not input_str:
        return await edit_delete(
            event, "᯽︙  پێویستە وەڵامی بەستەرەکە بدەیتەوە یان بەستەرەکە دابنێیت لەگەڵ فەرمانەکە", 5
        )
    check = url(input_str)
    if not check:
        catstr = "http://" + input_str
        check = url(catstr)
    if not check:
        return await edit_delete(event, "᯽︙  ئەم لینکە پشتگیری نەکراوە", 5)
    sample_url = f"https://da.gd/dns/{input_str}"
    response_api = requests.get(sample_url).text
    if response_api:
        await edit_or_reply(event, f"dns ... {input_str} ئەو \n\n{response_api}")
    else:
        await edit_or_reply(
            event, f"᯽︙ - نەمتوانی بیدۆزمەوە `{input_str}` لەئینتەرنێتدا"
        )

# urltools for iqub
@iqub.ar_cmd(
    pattern="short(?:\s|$)([\s\S]*)",
    command=("short", plugin_category),
    info={
        "header": "بۆ کورتکردنی بەستەری دراو.",
        "usage": "{tr}short <بەستەر/وەڵامدانەوەی بەستەر>",
        "examples": "{tr}short https://www.facebook.com/xv7amo?mibextid=ZbWKwL ",
    },
)
async def _(event):
    "shortens the given link"
    input_str = "".join(event.text.split(maxsplit=1)[1:])
    reply = await event.get_reply_message()
    if not input_str and reply:
        input_str = reply.text
    if not input_str:
        return await edit_delete(
            event, "᯽︙  پێویستە وەڵامی بەستەرەکە بدەیتەوە یان بەستەرەکە دابنێیت لەگەڵ فەرمانەکە", 5
        )
    check = url(input_str)
    if not check:
        catstr = f"http://" + input_str
        check = url(catstr)
    if not check:
        return await edit_delete(event, "᯽︙  ئەم لینکە پشتگیری نەکراوە", 5)
    if not input_str.startswith("http"):
        input_str = "http://" + input_str
    sample_url = f"https://da.gd/s?url={input_str}"
    response_api = requests.get(sample_url).text
    if response_api:
        await edit_or_reply(
            event, f"᯽︙ بەستەری کورتکراو دروست کرا: {response_api}", link_preview=False
        )
    else:
        await edit_or_reply(event, "᯽︙  شتێك هەڵەیە، دواتر هەوڵ بدە")

# urltools for iqub
  
@jepiq.ar_cmd(
    pattern="hide(?:\s|$)([\s\S]*)",
    command=("hide", plugin_category),
    info={
        "header": "بۆ شاردنەوەی بەستەرەکە لەگەڵ بۆشایی سپی بە بەکارهێنانی هایپەرلینك.",
        "usage": "{tr}hide <بەستەر/وەڵامدانەوەی بەستەر>",
        "examples": "{tr}hide https://da.gd/rm6qri",
    },
)
async def _(event):
    "To hide the url with white spaces using hyperlink."
    input_str = "".join(event.text.split(maxsplit=1)[1:])
    reply = await event.get_reply_message()
    if not input_str and reply:
        input_str = reply.text
    if not input_str:
        return await edit_delete(
            event, "᯽︙  پێویستە بەستەرەکە وەڵامی بەستەرەکە بدەیتەوە یان بەستەرەکە دابنێیت لەگەڵ فەرمانەکە", 5
        )
    check = url(input_str)
    if not check:
        catstr = "http://" + input_str
        check = url(catstr)
    if not check:
        return await edit_delete(event, "᯽︙  ئەم بەستەرە پشتگیری نەکراوە", 5)
    await edit_or_reply(event, "[ㅤㅤㅤㅤㅤㅤㅤ](" + input_str + ")")
