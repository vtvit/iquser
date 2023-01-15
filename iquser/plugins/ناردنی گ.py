#Fixed by Reda

import os

from telethon import events
from telethon.tl.functions.channels import EditAdminRequest
from telethon.tl.types import ChatAdminRights
from iquser import iqub

from ..core.managers import edit_or_reply

from . import *
plugin_category = "utils"

@iqub.iq_cmd(
    pattern="ناردنی گشتی ?(.*)$",
    command=("وجه", plugin_category),
)
async def gcast(event):
    if not event.out and not is_fullsudo(event.sender_id):
        return await edit_or_reply(event, "ئەمە سنووردارە")
    xx = event.pattern_match.group(1)
    if not xx:
        return edit_or_reply(event, "** ᯽︙ پێویستە دەقێك هەبێت لەگەڵ فەرمانەکە**")
    tt = event.text
    msg = tt[5:]
    event = await edit_or_reply(event, "** ᯽︙ ئێستا نامەکە دەنێردرێت بۆ گرووپەکان چاوەڕێ بکە**")
    er = 0
    done = 0
    async for x in bot.iter_dialogs():
        if x.is_group:
            chat = x.id
            try:
                done += 1
                await bot.send_message(chat, msg)
            except BaseException:
                er += 1
    await event.edit(f"بەسەرکەوتوویی لە {done} لە چاتەکەدا , هەڵەیە لە {er} لە چاتەکەدا")


@iqub.iq_cmd(
    pattern="ناردنی تایبەت ?(.*)$",
    command=("ناردنی تایبەت", plugin_category),
)
async def gucast(event):
    if not event.out and not is_fullsudo(event.sender_id):
        return await edit_or_reply(event, "ئەمە سنووردارە")
    xx = event.pattern_match.group(1)
    if not xx:
        return edit_or_reply(event, "** ᯽︙ پێویستە دەقێك هەبێت لەگەڵ فەرمانەکە**")
    tt = event.text
    msg = tt[6:]
    kk = await edit_or_reply(event, "** ᯽︙ نامەکە دەنێردرێت بۆ تایبەتی ئەو کەسانەی لاتن کەمێك چاوەڕێ بکە**")
    er = 0
    done = 0
    async for x in bot.iter_dialogs():
        if x.is_user and not x.entity.bot:
            chat = x.id
            try:
                done += 1
                await bot.send_message(chat, msg)
            except BaseException:
                er += 1
    await event.edit(f"بە سەرکەوتوویی لە {done} لە چاتەکەدا , هەڵەیە لە {er} لە چاتەکەدا")
