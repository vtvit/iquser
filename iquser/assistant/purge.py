#(c) Copyright IQuser 2020-21
#هەموو مافەکان پارێزراون بۆ سەرچاوەی بۆتی زیرەك
#By ~  @IQ7amo
import asyncio

from telethon import events
from telethon.errors.rpcerrorlist import MessageDeleteForbiddenError
from telethon.tl.types import ChannelParticipantsAdmins

from iquser import iqub
from .. import *

OWNER_ID = bot.uid
# بۆ دڵنیابوون لە دەسەڵاتەکانی بەڕێوبەر

async def is_administrator(user_id: int, message):
    admin = False
    async for user in tgbot.iter_participants(
        message.chat_id, filter=ChannelParticipantsAdmins
    ):
        if user_id == user.id or OWNER_ID or SUDO_USERS:
            admin = True
            break
    return admin


@tgbot.on(events.NewMessage(pattern="^/purge"))
async def purge(event):
    chat = event.chat_id
    msgs = []

    if not await is_administrator(user_id=event.sender_id, message=event):
        await event.reply("تۆ بەڕێوبەر نیت!")
        return

    msg = await event.get_reply_message()
    if not msg:
        await event.reply("وەڵامی ئەو نامەیە بدەوە کە دەتەوێت نامەکانی ژێری بسڕیتەوە.")
        return

    try:
        msg_id = msg.id
        count = 0
        to_delete = event.message.id - 1
        await tgbot.delete_messages(chat, event.message.id)
        msgs.append(event.reply_to_msg_id)
        for m_id in range(to_delete, msg_id - 1, -1):
            msgs.append(m_id)
            count += 1
            if len(msgs) == 100:
                await tgbot.delete_messages(chat, msgs)
                msgs = []

        await tgbot.delete_messages(chat, msgs)
        del_res = await tgbot.send_message(
            event.chat_id, f"پاککردنەوەی خێرا {count} نامە."
        )

        await asyncio.sleep(4)
        await del_res.delete()

    except MessageDeleteForbiddenError:
        text = "هەڵە هەیە لە سڕینەوەی نامەکان.\n"
        text += "نامەکە لەوانەیە کۆنتربێت یان تۆ مۆڵەتی سڕینەوەت نییە."
        del_res = await event.reply(text, parse_mode="md")
        await asyncio.sleep(5)
        await del_res.delete()


@tgbot.on(events.NewMessage(pattern="^/del$"))
async def delete_msg(event):

    if not await is_administrator(user_id=event.sender_id, message=event):
        await event.reply("تۆ بەڕێوبەر نیت!")
        return

    chat = event.chat_id
    msg = await event.get_reply_message()
    if not msg:
        await event.reply("وەڵامی ئەو نامەیە بدەوە کە دەتەوێت نامەکانی ژێری بسڕیتەوە")
        return
    to_delete = event.message
    chat = await event.get_input_chat()
    rm = [msg, to_delete]
    await tgbot.delete_messages(chat, rm)
