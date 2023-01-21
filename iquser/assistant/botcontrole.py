import asyncio
from datetime import datetime

from telethon.errors import BadRequestError, FloodWaitError, ForbiddenError

from iquser import iqub

from ..Config import Config
from ..core.logger import logging
from ..core.managers import edit_delete, edit_or_reply
from ..helpers import reply_id, time_formatter
from ..helpers.utils import _format
from ..sql_helper.bot_blacklists import check_is_black_list, get_all_bl_users
from ..sql_helper.bot_starters import del_starter_from_db, get_all_starters
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
from . import BOTLOG, BOTLOG_CHATID
from .botmanagers import (
    ban_user_from_bot,
    get_user_and_reason,
    progress_str,
    unban_user_from_bot,
)

LOGS = logging.getLogger(__name__)

plugin_category = "بۆت"
botusername = Config.TG_BOT_USERNAME
cmhd = Config.COMMAND_HAND_LER





@iqub.bot_cmd(
    pattern="^/broadcast$",
    from_users=Config.OWNER_ID,
)
async def bot_broadcast(event):
    replied = await event.get_reply_message()
    if not replied:
        return await event.reply("وەڵامدانەوەی نامەیەك بۆ پەخشکردنی یەکەم !")
    start_ = datetime.now()
    br_cast = await replied.reply("بۆ هەمووان پەخش دەکرێت...")
    blocked_users = []
    count = 0
    bot_users_count = len(get_all_starters())
    if bot_users_count == 0:
        return await event.reply("هیچ کەسێك بۆتت بەکارناهێنێت")
    users = get_all_starters()
    if users is None:
        return await event.reply("**هەڵەیەك هەیە لەکاتی پشکنینی لیستی بەکارهێنەران**")
    for user in users:
        try:
            await event.client.send_message(
                int(user.user_id), "🔊 تۆ پەخشێکی نوێت پێگەیشت"
            )
            await event.client.send_message(int(user.user_id), replied)
            await asyncio.sleep(0.8)
        except FloodWaitError as e:
            await asyncio.sleep(e.seconds)
        except (BadRequestError, ValueError, ForbiddenError):
            del_starter_from_db(int(user.user_id))
        except Exception as e:
            LOGS.error(str(e))
            if BOTLOG:
                await event.client.send_message(
                    BOTLOG_CHATID, f"**BOTLOG_CHATID, f"**هەڵە لەکاتی پەخشکردن**\n`{str(e)}`"
                )
        else:
            count += 1
            if count % 5 == 0:
                try:
                    prog_ = (
                        "🔊  پەخشکردن...\n\n"
                        + progress_str(
                            total=bot_users_count,
                            current=count + len(blocked_users),
                        )
                        + f"\n\n• ✔️🕷️ **سەرکەوتووبوو* :  `{count}`\n"
                        + f"• ✖️ **هەڵەیە** :  `{len(blocked_users)}`"
                    )
                    await br_cast.edit(prog_)
                except FloodWaitError as e:
                    await asyncio.sleep(e.seconds)
    end_ = datetime.now()
    b_info = f"🔊بە سەرکەوتوویی نامەی پەخشکراو بۆ ➜  <b>{count} بەکارهێنەران.</b>"
    if len(blocked_users) != 0:
        b_info += f"\n🚫  <b>{len(blocked_users)} لە بەکارهێنەرانەوە</b> ئەگەر نامەکە سڕایەوە ئەوا ئەو بۆت تۆی بلۆککرد."
    b_info += (
        f"\n⏳  <code> پڕۆسەکە ئەنجامدرا: {time_formatter((end_ - start_).seconds)}</code>."
    )
    await br_cast.edit(b_info, parse_mode="html")


@iqub.bot_cmd(
    pattern="users$",
    command=("users", plugin_category),
    info={
        "سەری پەڕە": "بۆ بەدەستھێنانی بەکارهێنەرانی بۆت",
        "وەسف": "بۆ بینینی لیستی ئەو بەکارهێنەرانەی کە بۆتەکەتیان چالاککردووە",
        "بەکارهێنان": "{tr}بەکارهێنەرەکان",
    },
)
async def ban_starters(event):
    "بۆ بەدەستھێنانی بەکارهێنەرانی بۆت."
    ulist = get_all_starters()
    if len(ulist) == 0:
        return await edit_delete(event, "** کەس بۆتەکەتیان بەکارنەھێنا.**")
    msg = "**لیستی بەکارهێنەرانی بۆت :\n\n**"
    for user in ulist:
        msg += f"•  👤 {_format.mentionuser(user.first_name , user.user_id)}\n**ناسنامە:** `{user.user_id}`\n**ناوی بەکارهێنەر:** @{user.username}\n**بەروار: **__{user.date}__\n\n"
    await edit_or_reply(event, msg)


@iqub.bot_cmd(
    pattern="^/ban\s+([\s\S]*)",
    from_users=Config.OWNER_ID,
)
async def ban_botpms(event):
    user_id, reason = await get_user_and_reason(event)
    reply_to = await reply_id(event)
    if not user_id:
        return await event.client.send_message(
            event.chat_id, "'(دەرکردنی)ناتوانم بەکارهێنەر بدۆزمەوە بۆ قەدەغەکردنی", reply_to=reply_to
        )
    if not reason:
        return await event.client.send_message(
            event.chat_id, "بۆ دەرکردنی کەسێك سەرەتا دەبێت هۆکارەکەی بنووسرێت", reply_to=reply_to
        )
    try:
        user = await event.client.get_entity(user_id)
        user_id = user.id
    except Exception as e:
        return await event.reply(f"**هەڵەیە:**\n`{str(e)}`")
    if user_id == Config.OWNER_ID:
        return await event.reply("ناتوانم خاوەنی بۆت بلۆك بکەم🕷️.")
    check = check_is_black_list(user.id)
    if check:
        return await event.client.send_message(
            event.chat_id,
            f"#پێشتر_قەدەغەکراوە(دەرکراوە)\
            \nئەم بەکارهێنەرە لە لیستی کەسە دەرکراوەکاندایە\
            \n**هۆکاری قەدەغەکردنت\دەرکردن:** `{check.reason}`\
            \n**بەروار:** `{check.date}`.",
        )
    msg = await ban_user_from_bot(user, reason, reply_to)
    await event.reply(msg)


@iqub.ar_cmd(
    pattern="^/unban(?:\s|$)([\s\S]*)",
    from_users=Config.OWNER_ID,
)
async def ban_botpms(event):
    user_id, reason = await get_user_and_reason(event)
    reply_to = await reply_id(event)
    if not user_id:
        return await event.client.send_message(
            event.chat_id, "** ناتوانم بەکارهێنەرەکە بدۆزمەوە بۆ لادانی دەرکردن🕷️.**", reply_to=reply_to
        )
    try:
        user = await event.client.get_entity(user_id)
        user_id = user.id
    except Exception as e:
        return await event.reply(f"**هەڵەیە:**\n`{str(e)}`")
    check = check_is_black_list(user.id)
    if not check:
        return await event.client.send_message(
            event.chat_id,
            f"#هەڵوەشاندنەوەی دەرکردن \
            \n👤 {_format.mentionuser(user.first_name , user.id)} بەسەرکەوتوویی دەرکردنی لادرا لە بوتەکەوە.",
        )
    msg = await unban_user_from_bot(user, reason, reply_to)
    await event.reply(msg)


@iqub.bot_cmd(
    pattern="دەرکراوەکان$",
    command=("دەرکراوەکان", plugin_category),
    info={
        "سەری پەڕە": "بۆ بینینی لیستی قەدەغەکراوەکان لە بۆتەکەت",
        "ڕوونکردنەوە": "بۆ بینینی لیستی قەدەغەکراوەکان\دەرکراوەکان لە بۆتەکەت🕷️",
        "بەکارهێنان": "{tr}قەدەغەکراوەکان",
    },
)
async def ban_starters(event):
    "بۆ بینینی لیستی دەرکراوەکان لە بۆتەکەت"
    ulist = get_all_bl_users()
    if len(ulist) == 0:
        return await edit_delete(event, "** هیچ کەسێك دەرنەکراوە لە بۆتەکەت لە ئێستادا**")
    msg = "**بەکارهێنەرانی قەدەغەکراو لە بۆتەکەت :\n\n**"
    for user in ulist:
        msg += f"• 👤 {_format.mentionuser(user.first_name , user.chat_id)}\n**ناسنامە:** `{user.chat_id}`\n**ناوی بەکارهێنەر:** @{user.username}\n**بەروار: **{user.date}\n**هۆکار:** {user.reason}\n\n"
    await edit_or_reply(event, msg)

@iqub.bot_cmd(
    pattern="دۆخی دووبارەکردنە(چالاک|ناچالاک)$",
    command=("دۆخی_دووبارەکردنەوە", plugin_category),
    info={
        "header": "بۆ چالاککردن و نا چالاککردنی دووبارە کردنەوە لە بۆتەکەت",
        "ڕوونکردنەوە": "🕷️ئەگەر بەکارهێنەرەکە 10 نامە دووبارە بکاتەوە یان چاکی بکاتەوە، بۆتەکە بلۆکی دەکات",
        "بەکارهێنان": [
            "{tr}دۆخی دووبارەکردنەوە چالاکە",
            "{tr}دۆخی دووبارەکردنەوە ناچالاکە",
        ],
    },
)
async def ban_antiflood(event):
    "بۆ چالاککردن و نا چالاککردنی دووبارەکردنەوە لە بۆتەکەت."
    input_str = event.pattern_match.group(1)
    if input_str == "چالاک":
        if gvarstatus("bot_antif") is not None:
            return await edit_delete(event, "`دژە دووبارەکردنەوەی بۆت پێشتر چالاککراوە`")
        addgvar("bot_antif", True)
        await edit_delete(event, "`دژە دووبارەکردنەوەی بۆت چالاککراوە`")
    elif input_str == "ناچالاک":
        if gvarstatus("bot_antif") is None:
            return await edit_delete(event, "`دژە دووبارەکردنەوەی بۆت پێشتر لە کارخراوە.`")
        delgvar("bot_antif")
        await edit_delete(event, "` دژە دووبارەکردنەوەی بۆت لە کارخراوە.`")
