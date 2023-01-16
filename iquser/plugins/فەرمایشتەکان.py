import random
from telethon import events
import random, re

from jepthon.utils import admin_cmd

import asyncio
from iquser import iqub
from iqub.razan._islam import *
from ..core.managers import edit_or_reply

plugin_category = "extra" 

#by ~ @IQ7amo
@iqub.iq_cmd(
    pattern="زکری بەیانیان",
    command=("زکری بەیانیان", plugin_category),)
async def _(event):
     if not event.text[0].isalpha() and event.text[0] not in ("/", "#", "@", "!"):
           roze = random.choice(razan)
           return await event.edit(f"{roze}")
#by ~ @VTVIT
@iqub.iq_cmd(
    pattern="زکری ئێوارە$",
    command=("زکری ئێوارە", plugin_category),)
async def _(event):
     if not event.text[0].isalpha() and event.text[0] not in ("/", "#", "@", "!"):
           ror = random.choice(roz)
           return await event.edit(f"{ror}")
            
#by ~ @VTVIT
@iqub.iq_cmd(
    pattern="فەرمایشتەکان$",
    command=("فەرمایشتەکان", plugin_category),)
async def _(event):
     if not event.text[0].isalpha() and event.text[0] not in ("/", "#", "@", "!"):
           me = random.choice(roza)
           return await event.edit(f"{me}")

@iqub.iq_cmd(
    pattern="زکری بەخەبەرهاتن$",
    command=("زکری بەخەبەرهاتن", plugin_category),)
async def _(event):
     if not event.text[0].isalpha() and event.text[0] not in ("/", "#", "@", "!"):
           az = random.choice(rozan)
           return await event.edit(f"{az}")
                     
@iqub.iq_cmd(
    pattern="زکری خەوتن$",
    command="زکری خەوتن", plugin_category),)
async def _(event):
     if not event.text[0].isalpha() and event.text[0] not in ("/", "#", "@", "!"):
           rr = random.choice(rozmuh)
           return await event.edit(f"{rr}")
           
@iqub.iq_cmd(
    pattern="زکری نوێژ$",
    command=("زکری نوێژ", plugin_category),)
async def _(event):
     if not event.text[0].isalpha() and event.text[0] not in ("/", "#", "@", "!"):
           rm = random.choice(rzane)
           return await event.edit(f"{rm}")


@iqub.iq_cmd(
    pattern="فەرمانی زکرەکان$",
    command=("فەرمانی زکرەکان", plugin_category),)
async def _(event):
    await event.edit(
    "لـیـسـتـی فـەرمـانـی فـەرمـایـشـتـەکان :\n➖➖➖➖➖➖➖➖➖➖➖➖➖\n ᯽︙ یەکێك لە مانەی خوارەوە دابگرە🖤\n\n- ( `.زکری بەیانیان` ) \n- ( `.زکری ئێوارە` )   \n- (`.زکری خەوتن`)\n- ( `.زکری نوێژ`) \n- ( `.زکری بەخەبرهاتن` ) \n- ( `.فەرمایشتەکان` )\n- ( `.زکرەکان` )\n- ( `.زکری عەسر` )\n\n➖➖➖➖➖➖➖➖➖➖➖➖➖\n⌔︙CH : @xv7amo"
            )           
