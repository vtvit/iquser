from datetime import datetime

from telethon.utils import get_display_name

from iquser import iqub
from iquser.core.logger import logging

from ..Config import Config
from ..core import CMD_INFO, PLG_INFO
from ..core.data import _sudousers_list, sudo_enabled_cmds
from ..core.managers import edit_delete, edit_or_reply
from ..helpers.utils import get_user_from_event, mentionuser
from ..sql_helper import global_collectionjson as sql
from ..sql_helper import global_list as sqllist
from ..sql_helper.globals import addgvar, delgvar, gvarstatus

plugin_category = "tools"

LOGS = logging.getLogger(__name__)

IDEV = gvarstatus("sudoenable") or "true"

vtvitDV_cmd = (
    "𓆩 [𝗦𝗼𝘂𝗿𝗰𝗲 𝙄𝙌𝙐𝙎𝙀𝙍 𝗖𝗼𝗻𝗳𝗶𝗴 - فـەرمـانـی یـاردەدەری گـەشەپێدەر](t.me/IQUSER0) 𓆪\n\n"
    "**✾╎فـەرمـانـی  زیادکردنی یـاریـدەدەری گـەشەپێدەر 🧑🏻‍💻✅ 🦾 :** \n"
    "**- دەست دابگرە لەسەر فەرمان و کۆپی بکە و دایبنێ** \n\n"
    "**⪼** `.زیادکردنی گەشەپێدەر` \n"
    "**- بـۆ زیـادکردنی یـاریـدەدەرێك بۆ بۆتەکەت** \n\n"
    "**⪼** `.لادانی گەشەپێدەر` \n"
    "**- بۆ لادانی کەسێك لە یاریدەدەری بۆتەکەت** \n\n"
    "**⪼** `.گەشەپێدەران` \n"
    "**- بـۆ پـیشـاندانی گـەشەپێدەرانی بـۆت 🧑🏻‍💻📑** \n\n"
    "**⪼** `.دۆخی گەشەپێدەر چالاک` \n"
    "**بۆ چالاککردنی دۆخی یاردەدەری گەشەپێدەر** \n\n"
    "**⪼** `.دۆخی گەشەپێدەر ناچالاک` \n"
    "**بۆ ناچالاککردنی دۆخی یاریدەدەری گەشەپێدەر** \n\n"
    "**⪼** `.کۆنتڕۆڵی گشتی` \n"
    "**- پێدانی کۆنتڕۆڵی گشتی دەسەڵاتەکانی فەرمانەکان بە گەشەپێدەر ✓** \n\n"
    "**⪼** `.کۆنتڕۆڵی پاراستن` \n"
    "**- اعطـاء پێدانی کۆنتڕۆڵی پاراستنی دەسەڵاتی فەرمانەکان بە گەشەپێدەر ✓** \n\n"
    "**⪼** `.کۆنتڕۆڵی` + ناوی فەرمان\n"
    "**- پێدانی کۆنتڕۆڵی دەسەڵاتی یەك فەرمان بە گەشەپێدەر .. بۆ نموونە (.کۆنتڕۆڵی پشکنین) (.کۆنتڕۆڵی گۆرانی)**\n\n"
    "**⪼** `.وەستاندنی کۆنتڕۆڵی گشتی` \n"
    "**- بۆ وەستاندنی دەسەڵاتی کۆنتڕۆڵی گشتی لە گەشەپێدەر ✓** \n\n"
    "**⪼** `.وەستاندنی کۆنتڕۆڵی پاراستن` \n"
    "**- بۆ وەستاندنی دەسەڵاتی کۆنتڕۆڵی پاراستن لە گەشەپێدەر  ✓** \n\n"
    "**⪼** `.وەستاندنی کۆنتڕۆڵ` + ناوی فەرمان  \n"
    "**- ايقـاف صلاحيـة التحكـم المعطـاه لـ امـر واحـد فقـط او عـدة اوامـر للمطـورين المرفـوعيـن ✓ .. مثـال (.وەستاندنی کۆنتڕۆڵی پشکنین) او (.وەستاندنی کۆنتڕۆڵی گۆرانی گۆرانیەکانم)** \n\n"
    "**⪼** `کۆنتڕۆڵکراو`  /  `.کۆنتڕۆڵی ناچالاک ` \n"
    "**- پۆ پیشاندانی لیستی ئەو فەرمانانەی کە ڕێپێدراون گەشەپێدەر کۆنتڕۆڵی بکات 🛃🚷** \n\n"
    "\n𓆩 [𐇮 ﮼ﺣّ͠ــەمــە 🇧🇷 𐇮](t.me/VTVIT) 𓆪"
)


async def _init() -> None:
    sudousers = _sudousers_list()
    Config.SUDO_USERS.clear()
    for user_d in sudousers:
        Config.SUDO_USERS.add(user_d)


def get_key(val):
    for key, value in PLG_INFO.items():
        for cmd in value:
            if val == cmd:
                return key
    return None


@iqub.iq_cmd(
    pattern="دۆخی گەشەپێدەر (چالاک|ناچالاک)$",
    command=("دۆخی گەشەپێدەر", plugin_category),
    info={
        "header": "بۆ چالاککردن/ناچالاککردنی دۆخی گەشەپێدەر کردنەوەی/قفڵی کۆنتڕۆڵکردن بۆ گەشەپێدەر",
        "بەکارهێنان": "{tr}دۆخی گەشەپێدەر چالاک / ناچالاک",
    },
)
async def chat_blacklist(event):
    "بۆ چالاککردنی/ناچالاککردنی دۆخی گەشەپێدەر وە کردنەوەی/قفڵی کۆنتڕۆڵکردن بۆ گەشەپێدەر"
    input_str = event.pattern_match.group(1)
    sudousers = _sudousers_list()
    if input_str == "چالاک":
        if gvarstatus("sudoenable") is not None:
            return await edit_delete(event, "**- دۆخی گەشەپێدەر پێشتر چالاککراوە ✓**")
        addgvar("sudoenable", "true")
        return await edit_or_reply(event, "**✾╎بە سەرکەوتوویی دۆخی یاریدەدەری گەشەپێدەر .. چالاککرا✓**\n**✾╎دەستپێدەکاتەوە بۆتی زیرەك کەمێك چاوەڕێ بکە ▬▭ ...**")
    if input_str == "ناچالاک":
        if gvarstatus("sudoenable") is None:
            return await edit_delete(event, "**- دۆخی گەشەپێدەر پێشتر ناچالاککراوە ✓**")
        delgvar("sudoenable")
        return await edit_or_reply(event, "**✾╎بە سەرکەوتوویی دۆخی یاریدەدەری گەشەپێدەر .. ناچالاککرا✓**\n**✾╎دەستپێدەکاتەوە بۆتی زیرەك کەمێك چاوەڕێ بکە ▬▭ ...**")


@iqub.iq_cmd(
    pattern="زیادکردنی گەشەپێدەر(?:\s|$)([\s\S]*)",
    command=("زیادکردنی گەشەپێدەر", plugin_category),
    info={
        "header": "بۆ زیادکردنی گەشەپێدەر لەبۆتەکەت",
        "بەکارهێنان": "{tr}زیادکردنی گەشەپێدەر بە وەڵامدانەوەی / ناوی بەکارهێنەر / ناسنامەکەی",
    },
)
async def add_sudo_user(event):
    "بۆ زیادکردنی گەشەپێدەر لە بۆتەکەت"
    replied_user, error_i_a = await get_user_from_event(event)
    if replied_user is None:
        return
    if replied_user.id == event.client.uid:
        return await edit_delete(event, "** ببوورە .. ناتوانی خۆت زیادبکەیت**")
    if replied_user.id in _sudousers_list():
        return await edit_delete(
            event,
            f"**✾╎بەکارهێنەر**  {mentionuser(get_display_name(replied_user),replied_user.id)}  **پێشتر لە لیستی گەشەپێدەری بۆت بووە 🧑🏻‍💻...**",
        )
    date = str(datetime.now().strftime("%B %d, %Y"))
    userdata = {
        "chat_id": replied_user.id,
        "chat_name": get_display_name(replied_user),
        "chat_username": replied_user.username,
        "date": date,
    }
    try:
        sudousers = sql.get_collection("sudousers_list").json
    except AttributeError:
        sudousers = {}
    sudousers[str(replied_user.id)] = userdata
    addgvar("sudoenable", "true")
    sudocmds = sudo_enabled_cmds()
    loadcmds = CMD_INFO.keys()
    if len(sudocmds) > 0:
        sqllist.del_keyword_list("sudo_enabled_cmds")
    for cmd in loadcmds:
        sqllist.add_to_list("sudo_enabled_cmds", cmd)
    sql.del_collection("sudousers_list")
    sql.add_collection("sudousers_list", sudousers, {})
    output = f"**✾╎زیادکرا**  {mentionuser(userdata['chat_name'],userdata['chat_id'])}  **یاریدەدەری گەشەپێدەر بۆ بۆتەکەت 🧑🏻‍💻...**\n\n"
    output += "**✾╎دەستپێدەکاتەوە بۆتی زیرەك 1-2 خولەك چاوڕێ بکە ▬▭ ...**"
    msg = await edit_or_reply(event, output)
    await event.client.reload(msg)


@iqub.iq_cmd(
    pattern="لادانی گەشەپێدەر(?:\s|$)([\s\S]*)",
    command=("لادانی گەشەپێدەر", plugin_category),
    info={
        "header": "بـۆ لادانی گەشەپێدەر لە بۆتەکەت",
        "بەکارهێنان": "{tr}لادانی گەشەپێدەر بە وەڵامدانەوەی / ناوی بەکارهێنەر / ناسنامەکەی",
    },
)
async def _(event):
    "بـۆ لادانی گەشەپێدەر لە بۆتەکەت"
    replied_user, error_i_a = await get_user_from_event(event)
    if replied_user is None:
        return
    try:
        sudousers = sql.get_collection("sudousers_list").json
    except AttributeError:
        sudousers = {}
    if str(replied_user.id) not in sudousers:
        return await edit_delete(
            event,
            f"** - بەکارهێنەر :** {mentionuser(get_display_name(replied_user),replied_user.id)} \n\n**- ئەو لە لیستی گەشەپێدەران نییە.**",
        )
    del sudousers[str(replied_user.id)]
    sql.del_collection("sudousers_list")
    sql.add_collection("sudousers_list", sudousers, {})
    output = f"**✾╎لادرا**  {mentionuser(get_display_name(replied_user),replied_user.id)}  **لە لیستی گەشەپێدەرانی بۆت 🧑🏻‍💻...**\n\n
    output += "**✾╎دەستپێدەکاتەوە بۆتی زیرەك 1-2 خولەك چاوەڕێ بکە ▬▭ ...**"
    msg = await edit_or_reply(event, output)
    await event.client.reload(msg)


@iqub.iq_cmd(
    pattern="گەشەپێدەران$",
    command=("گەشەپێدەران", plugin_category),
    info={
        "header": "بـۆ پیشاندانی لیستی گەشەپێدەرانی بۆت",
        "بەکارهێنەر": "{tr}گەشەپێدەران",
    },
)
async def _(event):
    "بۆ پیشاندانی لیستی گەشەپێدەرانی بۆت"
    sudochats = _sudousers_list()
    try:
        sudousers = sql.get_collection("sudousers_list").json
    except AttributeError:
        sudousers = {}
    if len(sudochats) == 0:
        return await edit_delete(
            event, "**•❐• هیچ گەشەپێدەرێك نییە لە بۆتەکەت لە ئێستادا**"
        )
    result = "**•❐• لیستی گەشەپێدەرانی بۆتی تایبەت بەتۆ 𝙄𝙌𝙐𝙎𝙀𝙍:**\n\n"
    for chat in sudochats:
        result += f"**🧑🏻‍💻╎گەشەپێدەران :** {mentionuser(sudousers[str(chat)]['chat_name'],sudousers[str(chat)]['chat_id'])}\n\n"
        result += f"**- بەروار زیادکرا :** {sudousers[str(chat)]['date']}\n\n"
    await edit_or_reply(event, result)


@iqub.iq_cmd(
    pattern="کۆنتڕۆڵی(s)?(?:\s|$)([\s\S]*)",
    command=("کۆنتڕۆڵی", plugin_category),
    info={
        "header": "To enable cmds for sudo users.",
        "flags": {
            "گشتی": "Will enable all cmds for sudo users. (except few like eval, exec, profile).",
            "هەموو": "Will add all cmds including eval,exec...etc. compelete sudo.",
            "فەرمان": "Will add all cmds from the given plugin names.",
        },
        "usage": [
            "{tr}کۆنتڕۆڵی پاراستن",
            "{tr}کۆنتڕۆڵی گشتی",
            "{tr}کۆنتڕۆڵی -p <ناوی فایل>",
            "{tr}کۆنتڕۆڵی <فەرمان>",
        ],
        "نموونە": [
            "{tr}addscmd -p autoprofile botcontrols i.e, for multiple names use space between each name",
            "{tr}addscmd ping alive i.e, for multiple names use space between each name",
        ],
    },
)
async def _(event):  # sourcery no-metrics
    "To enable cmds for sudo users."
    input_str = event.pattern_match.group(2)
    errors = ""
    sudocmds = sudo_enabled_cmds()
    if not input_str:
        return await edit_or_reply(
            event, "__Which command should i enable for sudo users . __"
        )
    input_str = input_str.split()
    if input_str[0] == "پاراستن":
        iqevent = await edit_or_reply(event, "**✾╎بە سەرکەوتوویی کۆنتڕۆڵی پاراستن بۆ گەشەپێدەر.. چالاککرا🧑🏻‍💻✅**")
        totalcmds = CMD_INFO.keys()
        flagcmds = (
            PLG_INFO["کۆنتڕۆڵی بۆت"]
            + PLG_INFO["کاتی"]
            + PLG_INFO["نوێکردنەوە"]
            + PLG_INFO["فەرمانەکان"]
            + PLG_INFO["هيروكو"]
            + PLG_INFO["بەڕێوبەر"]
            + PLG_INFO["پاراستن"]
            + PLG_INFO["گۆرانی"]
            + PLG_INFO["گرووپ"]
            + PLG_INFO["دەستپێکردنەوە"]
            + PLG_INFO["گۆڕین"]
            + PLG_INFO["گەشەپێدەر"]
            + PLG_INFO["بۆتی پاراستن"]
            + ["gauth"]
            + ["greset"]
        )
        loadcmds = list(set(totalcmds) - set(flagcmds))
        if len(sudocmds) > 0:
            sqllist.del_keyword_list("sudo_enabled_cmds")
    elif input_str[0] == "گشتی" or input_str[0] == "هەموو":
        iqevent = await edit_or_reply(
            event, "**✾╎بە سەرکەوتوویی دەسەڵاتی کۆنتڕۆڵی گشتی بۆگەشەپێدەر .. چالاککیا🧑🏻‍💻✅**"
        )
        loadcmds = CMD_INFO.keys()
        if len(sudocmds) > 0:
            sqllist.del_keyword_list("sudo_enabled_cmds")
    elif input_str[0] == "فایل":
        iqevent = event
        input_str.remove("فایل")
        loadcmds = []
        for plugin in input_str:
            if plugin not in PLG_INFO:
                errors += (
                    f"`{plugin}` __There is no such plugin in your iquser__.\n"
                )
            else:
                loadcmds += PLG_INFO[plugin]
    else:
        iqevent = event
        loadcmds = []
        for cmd in input_str:
            if cmd not in CMD_INFO:
                errors += f"**✾╎ببوورە .. هیچ فەرمانی بەناو نییە ** `{cmd}` **لە سەرچاوەکە**\n"
            elif cmd in sudocmds:
                errors += f"**✾╎کۆنتڕۆڵی فەرمان چالاککرا** `{cmd}` \n**✾╎بە سەرکەوتوویی بۆ هەموو گەشەپێدەرانی بۆت🧑🏻‍💻✅**\n"
            else:
                loadcmds.append(cmd)
    for cmd in loadcmds:
        sqllist.add_to_list("sudo_enabled_cmds", cmd)
    result = f"**✾╎تـم تفعيـل التحكـم الكـامل لـ**  `{len(loadcmds)}` **امـر 🧑🏻‍💻✅**\n"
    output = (
        result + "**✾╎يتم الان اعـادة تشغيـل بـوت زدثــون انتظـر 2-1 دقيقـه ▬▭ ...**\n"
    )
    if errors != "":
        output += "\n**- خطــأ :**\n" + errors
    msg = await edit_or_reply(zedevent, output)
    await event.client.reload(msg)


@zedub.zed_cmd(
    pattern="ايقاف تحكم(s)?(?:\s|$)([\s\S]*)?",
    command=("ايقاف تحكم", plugin_category),
    info={
        "header": "To disable given cmds for sudo.",
        "flags": {
            "-all": "Will disable all enabled cmds for sudo users.",
            "-flag": "Will disable all flaged cmds like eval, exec...etc.",
            "-p": "Will disable all cmds from the given plugin names.",
        },
        "الاستـخـدام": [
            "{tr}rmscmd -all",
            "{tr}rmscmd -flag",
            "{tr}rmscmd -p <plugin names>",
            "{tr}rmscmd <commands>",
        ],
        "مثــال": [
            "{tr}rmscmd -p autoprofile botcontrols i.e, for multiple names use space between each name",
            "{tr}rmscmd ping alive i.e, for multiple commands use space between each name",
        ],
    },
)
async def _(event):  # sourcery no-metrics
    "To disable cmds for sudo users."
    input_str = event.pattern_match.group(2)
    errors = ""
    sudocmds = sudo_enabled_cmds()
    if not input_str:
        return await edit_or_reply(
            event, "__Which command should I disable for sudo users . __"
        )
    input_str = input_str.split()
    if input_str[0] == "كامل" or input_str[0] == "الكل":
        zedevent = await edit_or_reply(
            event, "**✾╎تـم تعطيـل التحكـم الكـامـل للمطـوريـن لـ جميـع الاوامـر .. بنجـاح🧑🏻‍💻✅**"
        )
        flagcmds = sudocmds
    elif input_str[0] == "آمن":
        zedevent = await edit_or_reply(
            event, "**✾╎تـم تعطيـل التحكـم للمطـوريـن لـ الاوامـر الآمـنـه .. بنجـاح🧑🏻‍💻✅**"
        )
        flagcmds = (
            PLG_INFO["botcontrols"]
            + PLG_INFO["الوقتي"]
            + PLG_INFO["التحديث"]
            + PLG_INFO["الاوامر"]
            + PLG_INFO["هيروكو"]
            + PLG_INFO["الادمن"]
            + PLG_INFO["الحمايه"]
            + PLG_INFO["الاغاني"]
            + PLG_INFO["المجموعه"]
            + PLG_INFO["اعاده تشغيل"]
            + PLG_INFO["تحويل الصيغ"]
            + PLG_INFO["المطور"]
            + PLG_INFO["بوت الحمايه"]
            + ["gauth"]
            + ["greset"]
        )
    elif input_str[0] == "ملف":
        zedevent = event
        input_str.remove("ملف")
        flagcmds = []
        for plugin in input_str:
            if plugin not in PLG_INFO:
                errors += (
                    f"`{plugin}` __There is no such plugin in your ZThon__.\n"
                )
            else:
                flagcmds += PLG_INFO[plugin]
    else:
        zedevent = event
        flagcmds = []
        for cmd in input_str:
            if cmd not in CMD_INFO:
                errors += f"**✾╎عـذراً .. لايـوجـد امـر بـ اسـم** `{cmd}` **فـي السـورس**\n"
            elif cmd not in sudocmds:
                errors += f"**✾╎تـم تعطيـل التحكـم بـ امـر** `{cmd}` \n**✾╎لجميـع مطـوريـن البـوت .. بنجـاح🧑🏻‍💻✅**\n"
            else:
                flagcmds.append(cmd)
    count = 0
    for cmd in flagcmds:
        if sqllist.is_in_list("sudo_enabled_cmds", cmd):
            count += 1
            sqllist.rm_from_list("sudo_enabled_cmds", cmd)
    result = f"**✾╎تـم تعطيـل التحكـم الكـامل لـ**  `{count}` **امـر 🧑🏻‍💻✅**\n"
    output = (
        result + "**✾╎يتم الان اعـادة تشغيـل بـوت زدثــون انتظـر 2-1 دقيقـه ▬▭ ...**\n"
    )
    if errors != "":
        output += "\n**- خطــأ :**\n" + errors
    msg = await edit_or_reply(zedevent, output)
    await event.client.reload(msg)


@zedub.zed_cmd(
    pattern="التحكم( المعطل)?$",
    command=("التحكم", plugin_category),
    info={
        "header": "To show list of enabled cmds for sudo.",
        "description": "will show you the list of all enabled commands",
        "flags": {"-d": "To show disabled cmds instead of enabled cmds."},
        "الاستـخـدام": [
            "{tr}التحكم",
            "{tr}التحكم المعطل",
        ],
    },
)
async def _(event):  # sourcery no-metrics
    "To show list of enabled cmds for sudo."
    input_str = event.pattern_match.group(1)
    sudocmds = sudo_enabled_cmds()
    clist = {}
    error = ""
    if not input_str:
        text = "**•🧑🏻‍💻• قائمــة الاوامـر المسمـوحـه لـ المطـوريـن المـرفـوعيـن فـي البـوت الخـاص بـك 🏧:**"
        result = "**- اوامـر تحكـم المطـوريـن 🛃**"
        if len(sudocmds) > 0:
            for cmd in sudocmds:
                plugin = get_key(cmd)
                if plugin in clist:
                    clist[plugin].append(cmd)
                else:
                    clist[plugin] = [cmd]
        else:
            error += "**✾╎عـذراً .. لايـوجـد اي اوامـر تحكـم خاصـه بـ المطـوريـن**\n**✾╎بنێرە (** `.یارمەتیدان` **) لـ تصفـح اوامـر التحكـم 🛂**"
        count = len(sudocmds)
    else:
        text = "**•🧑🏻‍💻• لیستی فەرمانەکان ڕێگە پێنەدراوە 📵 بۆ گەشەپێدەران کە بارکراون لە بۆتەکەت :**"
        result = "**- فەرمانەکانی کۆنتڕۆڵی کەمی گەشەپێدەر 🚸**"
        totalcmds = CMD_INFO.keys()
        cmdlist = list(set(totalcmds) - set(sudocmds))
        if cmdlist:
            for cmd in cmdlist:
                plugin = get_key(cmd)
                if plugin in clist:
                    clist[plugin].append(cmd)
                else:
                    clist[plugin] = [cmd]
        else:
            error += "**✾╎کۆنترۆڵی تەواوی هەموو فەرمانەکانی بۆت بۆ گەشەپێدەران**\n**✾╎هیچ فەرمانێکی ناچالاك نیە بۆ دەستگەیشتنی گەشەپێدەر بۆ ئەوان**\n\n**✾╎بنێرە (** `.یارمەتیدان` **) بۆ گەڕانی فەرمانەکانی وەستانی کۆنترۆڵ  🚷**"
        count = len(cmdlist)
    if error != "":
        return await edit_delete(event, error, 10)
    pkeys = clist.keys()
    n_pkeys = [i for i in pkeys if i is not None]
    pkeys = sorted(n_pkeys)
    output = ""
    for plugin in pkeys:
        output += f"• {plugin}\n"
        for cmd in clist[plugin]:
            output += f"`{cmd}` "
        output += "\n\n"
    finalstr = (
        result
        + f"\n\n**-  خاڵەکانی فەرمانی گەشەپێدەر بریتیە لە : **`{Config.SUDO_COMMAND_HAND_LER}`\n**- ژمارەی فەرمانەکان :** {count}\n\n"
        + output
    )
    await edit_or_reply(event, finalstr, aslink=True, linktext=text)


iqub.loop.create_task(_init())



# Copyright (C) 2022 IqUser . All Rights Reserved
@iqub.iq_cmd(pattern="یارمەتیدان")
async def cmd(vtvit):
    await edit_or_reply(vtvit, vtvitDV_cmd)


