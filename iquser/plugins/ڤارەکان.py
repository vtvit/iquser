# vtvit
# Copyright (C) 2022 vtvit . All Rights Reserved
#
# This file is a part of < https://github.com/vtvit/iquser/ >
# PLease read the GNU Affero General Public License in
# <https://github.com/vtvit/iquser/blob/main/LICENSE>.

""" وەسفی فایل : فەرمانی زیادکردنی وێنە و دەق لە ڤارەکان ( پاراستن - پشکنین - کاتی ) امـر واحـد فقـط
 : @IQUSER0
@VTVIT - نوسینی :  ئێرن """
#مناڵ هههههههههههههههههههههههههه

import asyncio
import math
import os

import heroku3
import requests
import urllib3
from datetime import datetime

from PIL import Image
from telegraph import Telegraph, exceptions, upload_file
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import MessageEntityMentionName

from iquser import iqub

from ..Config import Config
from ..core.managers import edit_delete, edit_or_reply
from ..sql_helper.globals import addgvar, delgvar, gvarstatus

Heroku = heroku3.from_key(Config.HEROKU_API_KEY)
heroku_api = "https://api.heroku.com"
HEROKU_APP_NAME = Config.HEROKU_APP_NAME
HEROKU_API_KEY = Config.HEROKU_API_KEY
from . import BOTLOG_CHATID, mention


plugin_category = "ئامێرەکان"


telegraph = Telegraph()
r = telegraph.create_account(short_name=Config.TELEGRAPH_SHORT_NAME)
auth_url = r["auth_url"]


iquserVP_cmd = (
    "𓆩 [𝗦𝗼𝘂𝗿𝗰𝗲 𝙄𝙌 𝙐𝙎𝙀𝙍 ࿐ 𝗖𝗼𝗻𝗳𝗶𝗴 𝗩𝗮𝗿𝘀 - فەرمانی ڤارەکان](t.me/IQUSER0) 𓆪\n\n"
    "**✾╎لیستی گۆڕینی فەرمانی ڤار   -  بۆ یەکەم جار سەرچاوەی بۆتی زیرەك 🦾 :** \n\n"
    "⪼ `.زیادکردنی وێنەی پاراستن` بە وەڵامدانەوەێ وێنە یان میدیا\n\n"
    "⪼ `.زیادکردنی وێنەی پشکنین` بە وەڵامدانەوەی وێنە یان میدیا  \n\n"
    "⪼ `.زیادکردنی وێنەی کاتی` بە وەڵامدانەوەی وێنە یان ميديـا\n\n"
    "⪼ `.زیادکردنی وێنەی فەرمانەکان  ` بە وەڵامدانەوەی وێنە یان میدیا \n\n"
    "⪼ `.زیادکردنی وێنەی سەرچاوا` بە وەڵامدانەوەی وێنە یان میدیا \n\n"
    "⪼ `.زیادکردنی وێنەی ئاگاداری` بە وەڵامدانەوەی وێنە یان میدیا \n\n"
    "⪼ `.زیادکردنی وێنەی بۆت` بە وەڵامدانەوەی وێنە یان میدیا  بۆ زیادکردنی وێنەی بۆتە کاتێ start دەکەیت\n\n"
    "فەرمانی ڤارەکان` بۆ بینینی زیاتر لە فەرمانی ڤار \n\n\n"
    "**✾╎لیستی فەرمانی گۆڕینی کلایشی ناسنامە :** \n\n"
    "⪼ `.زیادکردنی ئیمۆجی ناسنامە` بە وەڵامدانەوەی ڕەمز یان ئیمۆجی \n\n"
    "⪼ `.زیادکردنی ناونیشانی ناسنامە` بە وەڵامدانەوەی دەقی ناونیشان\n\n"
    "⪼ `.زیادکردنی هێڵی ناسنامە` بە وەڵامدانەوەی هێڵ یان ڕاستەهێڵ \n\n\n"
    "**✾╎لیستی فەرمانی گۆڕینی ڤارەکانی تر :** \n\n"
    "⪼ `.زیادکردنی کلایشی پاراستن` بە وەڵامدانەوەی کلایش\n\n"
    "⪼ `.زیادکردنی کلایشی پشکنین` بە وەڵامدانەوەی کلایشەکە\n\n"
    "⪼ `.زیادکردنی کلایشی دەرکردن` بە وەڵامدانەوەی کلایشەکە \n\n"
    "⪼ `.زیادکردنی کلایشی بۆت ` بە وەڵامدانەوەی کلایشەکە بۆ زیادبوونی کلایشی ستارت\n\n"
    "⪼ `.زیادکردنی ڕەمزی کاتی` بە وەڵامدانەوەی ڕەمز\n\n"
    "⪼ `.زیادکردنی زەخرەفەی کات` بە وەڵامدانەوەی زەخرەفە\n\n"
    "⪼ `.زیادکردنی بایۆی کاتی` بە وەڵامدانەوەی بایۆکەت \n\n"
    "⪼ `.زیادکردنی ناوی بەکارهێنەر` بە وەڵامدانەوەی ناو \n\n"
    "⪼ `.زیادکردنی گرووپی سەیڤ` بە وەڵامدانەوەی ناسنامەی گرووپ \n\n"
    "⪼ `.زیادکردنی گرووپی ئاگاداریەکان` بە وەڵامدانەوەی ناسنامەی گرووپ\n\n"
    "⪼ `.زیادکردنی ناسنامە` بە وەڵامدانەوەی ناسنامەی ئەکاونتت\n\n"
    "⪼ `.زیادکردنی خاڵی فەرمان` بە وەڵامدانەوەی ڕەمزی نوێ \n\n"
    "⪼ `.زیادکردنی نامەی پاراستن` بە وەڵامدانەوەی ژمارەیەك بۆ ژمارەی نامەی ئاگادارکردنەوەی پاراستنی تایبەت\n\n\n"
    "⪼ `.بمدەرێ` + ناو ڤار\n\n"
    "⪼ `.سڕینەوەی` + ناو ڤار\n\n"
    "⪼ `.زیادکردنی گەشەپێدەر `بە وەڵامدانەوەی کەسێك بۆ ئەوەی ببێت بە گەشەپێدەر و کۆنتڕۆڵی گشت فەرمانەکان بکات\n\n"
    "⪼ `.سڕینەوەی گەشەپێدەران`\n\n"
    "**✾╎لیستی فەرمانی گۆڕینی شوێنی کات بۆ کات 🌐:** \n\n"
    "⪼ `.کاتی عراق` \n\n"
    "⪼ `.کاتی یەمەن` \n\n"
    "⪼ `.کاتی سوریا` \n\n"
    "⪼ `.کاتی مصر` \n\n"
    "🛃بەم نزیکانە وڵاتانی زیاتر زیاد دەکرێن\n\n"
    "\n𓆩 [𝑰𝑸 𝙑𝙖𝙧𝙨 - چەناڵی ڤارەکان](t.me/MGIMT) 𓆪"
)


# Copyright (C) 2022 Zed-Thon . All Rights Reserved
@zedub.zed_cmd(pattern=r"زیادکردنی (.*)")
async def variable(event):
    input_str = event.pattern_match.group(1)
    reply = await event.get_reply_message()
    vinfo = reply.text
    zed = await edit_or_reply(event, "**✾╎جـاري اضـافة الفـار الـى بـوتك ...**")
    # All Rights Reserved for "Zed-Thon" "زلـزال الهيبـه"
    if input_str == "كليشة الفحص" or input_str == "كليشه الفحص":
        variable = "ALIVE_TEMPLATE"
        await asyncio.sleep(1.5)
        if gvarstatus("ALIVE_TEMPLATE") is None:
            await zed.edit("**✾╎تم تغييـر {} بنجـاح ☑️**\n**✾╎الكليشـة الجـديده** \n {} \n\n**✾╎الان قـم بـ ارسـال الامـر ↶** `.فحص` **لـ التحقـق مـن الكليشـة . .**".format(input_str, vinfo))
        else:
            await zed.edit("**✾╎تم اضـافـة {} بنجـاح ☑️**\n**✾╎الكليشـة المضـافه** \n {} \n\n**✾╎الان قـم بـ ارسـال الامـر ↶** `.فحص` **لـ التحقـق مـن الكليشـة . .**".format(input_str, vinfo))
        addgvar("ALIVE_TEMPLATE", vinfo)
    elif input_str == "كليشة الحماية" or input_str == "كليشه الحمايه" or input_str == "كليشه الحماية" or input_str == "كليشة الحمايه":
        variable = "pmpermit_txt"
        await asyncio.sleep(1.5)
        if gvarstatus("pmpermit_txt") is None:
            await zed.edit("**✾╎تم تغييـر {} بنجـاح ☑️**\n**✾╎الكليشـة الجـديده** \n {} \n\n**✾╎الان قـم بـ ارسـال الامـر ↶** `.الحمايه تفعيل` **لـ التحقـق مـن الكليشـة . .**".format(input_str, vinfo))
        else:
            await zed.edit("**✾╎تم اضـافـة {} بنجـاح ☑️**\n**✾╎الكليشـة المضـافه** \n {} \n\n**✾╎الان قـم بـ ارسـال الامـر ↶** `.الحمايه تفعيل` **لـ التحقـق مـن الكليشـة . .**".format(input_str, vinfo))
        addgvar("pmpermit_txt", vinfo)
    elif input_str == "كليشة البوت" or input_str == "كليشه البوت":
        variable = "START_TEXT"
        await asyncio.sleep(1.5)
        if gvarstatus("START_TEXT") is None:
            await zed.edit("**✾╎تم تغييـر {} بنجـاح ☑️**\n**✾╎الكليشـة الجـديده** \n {} \n\n**✾╎الان قـم بـ الذهـاب لبوتك المسـاعد من حساب آخر ↶** ودز ستارت **لـ التحقـق مـن الكليشـة . .**".format(input_str, vinfo))
        else:
            await zed.edit("**✾╎تم اضـافـة {} بنجـاح ☑️**\n**✾╎الكليشـة المضـافه** \n {} \n\n**✾╎الان قـم بـ الذهـاب لبوتك المسـاعد من حساب آخر ↶** ودز ستارت **لـ التحقـق مـن الكليشـة . .**".format(input_str, vinfo))
        addgvar("START_TEXT", vinfo)
    elif input_str == "كليشة الحظر" or input_str == "كليشه الحظر":
        variable = "pmblock"
        await asyncio.sleep(1.5)
        if gvarstatus("pmblock") is None:
            await zed.edit("**✾╎تم تغييـر {} بنجـاح ☑️**\n**✾╎الكليشـة الجـديده** \n {} \n\n**✾╎الان قـم بـ الذهـاب لبوتك المسـاعد من حساب آخر ↶** ودز ستارت **لـ التحقـق مـن الكليشـة . .**".format(input_str, vinfo))
        else:
            await zed.edit("**✾╎تم اضـافـة {} بنجـاح ☑️**\n**✾╎الكليشـة المضـافه** \n {} \n\n**✾╎الان قـم بـ الذهـاب لبوتك المسـاعد من حساب آخر ↶** ودز ستارت **لـ التحقـق مـن الكليشـة . .**".format(input_str, vinfo))
        addgvar("pmblock", vinfo)
    elif input_str == "رمز الوقتي" or input_str == "رمز الاسم الوقتي":
        variable = "CUSTOM_ALIVE_EMZED"
        await asyncio.sleep(1.5)
        if gvarstatus("CUSTOM_ALIVE_EMZED") is None:
            addgvar(variable, vinfo)
            await zed.edit("**✾╎تم تغييـر {} بنجـاح ☑️**\n**✾╎الـرمـز الجـديـد** \n {} \n\n**✾╎الان قـم بـ ارسـال الامـر ↶** `.الاسم تلقائي` **لـ التحقـق مـن الـرمز . .**".format(input_str, vinfo))
        else:
            addgvar(variable, vinfo)
            await zed.edit("**✾╎تم اضـافـة {} بنجـاح ☑️**\n**✾╎الـرمـز المضـاف** \n {} \n\n**✾╎الان قـم بـ ارسـال الامـر ↶** `.الاسم تلقائي` **لـ التحقـق مـن الـرمز . .**".format(input_str, vinfo))
    elif input_str == "البايو" or input_str == "البايو الوقتي" or input_str == "النبذه" or input_str == "البايو تلقائي":
        variable = "DEFAULT_BIO"
        await asyncio.sleep(1.5)
        if gvarstatus("DEFAULT_BIO") is None:
            addgvar(variable, vinfo)
            await zed.edit("**✾╎تم تغييـر {} بنجـاح ☑️**\n**✾╎البـايـو الجـديـد** \n {} \n\n**✾╎الان قـم بـ ارسـال الامـر ↶** `.البايو تلقائي` **لـ التحقـق مـن البايـو . .**".format(input_str, vinfo))
        else:
            addgvar(variable, vinfo)
            await zed.edit("**✾╎تم اضـافه {} بنجـاح ☑️**\n**✾╎البـايـو المضـاف** \n {} \n\n**✾╎الان قـم بـ ارسـال الامـر ↶** `.البايو تلقائي` **لـ التحقـق مـن البايـو . .**".format(input_str, vinfo))
    elif input_str == "كاشف الاباحي" or input_str == "كشف الاباحي":
        variable = "DEEP_API"
        await asyncio.sleep(1.5)
        if gvarstatus("DEEP_API") is None:
            addgvar(variable, vinfo)
            await zed.edit("**✾╎تم تغييـر توكـن {} بنجـاح ☑️**\n**✾╎التوكـن الجـديـد** \n {} \n\n**✾╎الان قـم بـ ارسـال الامـر ↶** `.قفل الاباحي` **لـ تفعيـل كاشـف الاباحي . .**".format(input_str, vinfo))
        else:
            addgvar(variable, vinfo)
            await zed.edit("**✾╎تم إضافـة توكـن {} بنجـاح ☑️**\n**✾╎التوكـن المضـاف** \n {} \n\n**✾╎الان قـم بـ ارسـال الامـر ↶** `.قفل الاباحي` **لـ تفعيـل كاشـف الاباحي . .**".format(input_str, vinfo))
    elif input_str == "رسائل الحماية" or input_str == "رسائل الحمايه" or input_str == "رسائل الخاص" or input_str == "رسائل حماية الخاص" or input_str == "عدد التحذيرات":
        variable = "MAX_FLOOD_IN_PMS"
        await asyncio.sleep(1.5)
        if gvarstatus("MAX_FLOOD_IN_PMS") is None:
            await zed.edit("**✾╎تم تغييـر {} بنجـاح ☑️**\n\n**✾╎المتغيـر : ↶**\n `{}`\n**✾╎ارسـل الان** `.الحمايه تفعيل`".format(input_str, vinfo))
        else:
            await zed.edit("**✾╎تم تغييـر {} بنجـاح ☑️**\n\n**✾╎المتغيـر : ↶**\n `{}`\n**✾╎ارسـل الان** `.الحمايه تفعيل`".format(input_str, vinfo))
        addgvar("MAX_FLOOD_IN_PMS", vinfo)
    elif input_str == "ايموجي الايدي" or input_str == "ايموجي ايدي" or input_str == "رمز الايدي" or input_str == "رمز ايدي" or input_str == "الرمز ايدي":
        variable = "CUSTOM_ALIVE_EMOJI"
        await asyncio.sleep(1.5)
        if gvarstatus("CUSTOM_ALIVE_EMOJI") is None:
            await zed.edit("**✾╎تم تغييـر {} بنجـاح ☑️**\n\n**✾╎المتغيـر : ↶**\n `{}`\n**✾╎ارسـل الان** `.ايدي`".format(input_str, vinfo))
        else:
            await zed.edit("**✾╎تم تغييـر {} بنجـاح ☑️**\n\n**✾╎المتغيـر : ↶**\n `{}`\n**✾╎ارسـل الان** `.ايدي`".format(input_str, vinfo))
        addgvar("CUSTOM_ALIVE_EMOJI", vinfo)
    elif input_str == "عنوان الايدي" or input_str == "عنوان ايدي":
        variable = "CUSTOM_ALIVE_TEXT"
        await asyncio.sleep(1.5)
        if gvarstatus("CUSTOM_ALIVE_TEXT") is None:
            await zed.edit("**✾╎تم تغييـر {} بنجـاح ☑️**\n\n**✾╎المتغيـر : ↶**\n `{}`\n**✾╎ارسـل الان** `.ايدي`".format(input_str, vinfo))
        else:
            await zed.edit("**✾╎تم تغييـر {} بنجـاح ☑️**\n\n**✾╎المتغيـر : ↶**\n `{}`\n**✾╎ارسـل الان** `.ايدي`".format(input_str, vinfo))
        addgvar("CUSTOM_ALIVE_TEXT", vinfo)
    elif input_str == "خط الايدي" or input_str == "خط ايدي" or input_str == "خطوط الايدي" or input_str == "خط ايدي":
        variable = "CUSTOM_ALIVE_FONT"
        await asyncio.sleep(1.5)
        if gvarstatus("CUSTOM_ALIVE_FONT") is None:
            await zed.edit("**✾╎تم تغييـر {} بنجـاح ☑️**\n\n**✾╎المتغيـر : ↶**\n `{}`\n**✾╎ارسـل الان** `.ايدي`".format(input_str, vinfo))
        else:
            await zed.edit("**✾╎تم تغييـر {} بنجـاح ☑️**\n\n**✾╎المتغيـر : ↶**\n `{}`\n**✾╎ارسـل الان** `.ايدي`".format(input_str, vinfo))
        addgvar("CUSTOM_ALIVE_FONT", vinfo)
    elif input_str == "اسم المستخدم" or input_str == "الاسم":
        if Config.HEROKU_API_KEY is None:
            return await ed(event, "✾╎اضبط Var المطلوب في Heroku على وظيفة هذا بشكل طبيعي `HEROKU_API_KEY` اذا كنت لاتعلم اين يوجد فقط اذهب الى حسابك في هيروكو ثم الى الاعدادات ستجده بالاسفل انسخه ودخله في الفار. ")

        if Config.HEROKU_APP_NAME is not None:
            app = Heroku.app(Config.HEROKU_APP_NAME)
        else:
            return await ed(event, "✾╎اضبط Var المطلوب في Heroku على وظيفة هذا بشكل طبيعي `HEROKU_APP_NAME` اسم التطبيق اذا كنت لاتعلم.")
        heroku_var = app.config()
        variable = "ALIVE_NAME"
        await asyncio.sleep(1.5)
        if variable in heroku_var:
            await zed.edit("**✾╎تم تغييـر {} بنجـاح ☑️**\n**✾╎المتغيـر : ↶**\n `{}` \n**✾╎يتم الان اعـادة تشغيـل بـوت زد ثـون يستغـرق الامر 2-1 دقيقـه ▬▭ ...**".format(input_str, vinfo))
        else:
            await zed.edit("**✾╎تم اضافـة {} بنجـاح ☑️** \n**✾╎المضاف اليه :**\n `{}` \n**✾╎يتم الان اعـادة تشغيـل بـوت زد ثـون يستغـرق الامر 2-1 دقيقـه ▬▭ ...**".format(input_str, vinfo))
        heroku_var[variable] = vinfo
    elif input_str == "كروب الرسائل" or input_str == "كروب التخزين" or input_str == "كروب الخاص":
        if Config.HEROKU_API_KEY is None:
            return await ed(event, "✾╎اضبط Var المطلوب في Heroku على وظيفة هذا بشكل طبيعي `HEROKU_API_KEY` اذا كنت لاتعلم اين يوجد فقط اذهب الى حسابك في هيروكو ثم الى الاعدادات ستجده بالاسفل انسخه ودخله في الفار. ")

        if Config.HEROKU_APP_NAME is not None:
            app = Heroku.app(Config.HEROKU_APP_NAME)
        else:
            return await ed(event, "✾╎اضبط Var المطلوب في Heroku على وظيفة هذا بشكل طبيعي `HEROKU_APP_NAME` اسم التطبيق اذا كنت لاتعلم.")
        heroku_var = app.config()
        variable = "PM_LOGGER_GROUP_ID"
        await asyncio.sleep(1.5)
        if variable in heroku_var:
            await zed.edit("**✾╎تم تغييـر {} بنجـاح ☑️**\n**✾╎المتغيـر : ↶**\n `{}` \n**✾╎يتم الان اعـادة تشغيـل بـوت زد ثـون يستغـرق الامر 2-1 دقيقـه ▬▭ ...**".format(input_str, vinfo))
        else:
            await zed.edit("**✾╎تم اضافـة {} بنجـاح ☑️** \n**✾╎المضاف اليه :**\n `{}` \n**✾╎يتم الان اعـادة تشغيـل بـوت زد ثـون يستغـرق الامر 2-1 دقيقـه ▬▭ ...**".format(input_str, vinfo))
        heroku_var[variable] = vinfo
    elif input_str == "السجل" or input_str == "كروب السجل":
        if Config.HEROKU_API_KEY is None:
            return await ed(event, "✾╎اضبط Var المطلوب في Heroku على وظيفة هذا بشكل طبيعي `HEROKU_API_KEY` اذا كنت لاتعلم اين يوجد فقط اذهب الى حسابك في هيروكو ثم الى الاعدادات ستجده بالاسفل انسخه ودخله في الفار. ")

        if Config.HEROKU_APP_NAME is not None:
            app = Heroku.app(Config.HEROKU_APP_NAME)
        else:
            return await ed(event, "✾╎اضبط Var المطلوب في Heroku على وظيفة هذا بشكل طبيعي `HEROKU_APP_NAME` اسم التطبيق اذا كنت لاتعلم.")
        heroku_var = app.config()
        variable = "PRIVATE_GROUP_BOT_API_ID"
        await asyncio.sleep(1.5)
        if variable in heroku_var:
            await zed.edit("**✾╎تم تغييـر {} بنجـاح ☑️**\n**✾╎المتغيـر : ↶**\n `{}` \n**✾╎يتم الان اعـادة تشغيـل بـوت زد ثـون يستغـرق الامر 2-1 دقيقـه ▬▭ ...**".format(input_str, vinfo))
        else:
            await zed.edit("**✾╎تم اضافـة {} بنجـاح ☑️** \n**✾╎المضاف اليه :**\n `{}` \n**✾╎يتم الان اعـادة تشغيـل بـوت زد ثـون يستغـرق الامر 2-1 دقيقـه ▬▭ ...**".format(input_str, vinfo))
        heroku_var[variable] = vinfo
    elif input_str == "السجل 2" or input_str == "كروب السجل 2":
        if Config.HEROKU_API_KEY is None:
            return await ed(event, "✾╎اضبط Var المطلوب في Heroku على وظيفة هذا بشكل طبيعي `HEROKU_API_KEY` اذا كنت لاتعلم اين يوجد فقط اذهب الى حسابك في هيروكو ثم الى الاعدادات ستجده بالاسفل انسخه ودخله في الفار. ")

        if Config.HEROKU_APP_NAME is not None:
            app = Heroku.app(Config.HEROKU_APP_NAME)
        else:
            return await ed(event, "✾╎اضبط Var المطلوب في Heroku على وظيفة هذا بشكل طبيعي `HEROKU_APP_NAME` اسم التطبيق اذا كنت لاتعلم.")
        heroku_var = app.config()
        variable = "PRIVATE_GROUP_ID"
        await asyncio.sleep(1.5)
        if variable in heroku_var:
            await zed.edit("**✾╎تم تغييـر {} بنجـاح ☑️**\n**✾╎المتغيـر : ↶**\n `{}` \n**✾╎يتم الان اعـادة تشغيـل بـوت زد ثـون يستغـرق الامر 2-1 دقيقـه ▬▭ ...**".format(input_str, vinfo))
        else:
            await zed.edit("**✾╎تم اضافـة {} بنجـاح ☑️** \n**✾╎المضاف اليه :**\n `{}` \n**✾╎يتم الان اعـادة تشغيـل بـوت زد ثـون يستغـرق الامر 2-1 دقيقـه ▬▭ ...**".format(input_str, vinfo))
        heroku_var[variable] = vinfo
    elif input_str == "قناة السجل" or input_str == "قناة السجلات":
        if Config.HEROKU_API_KEY is None:
            return await ed(event, "✾╎اضبط Var المطلوب في Heroku على وظيفة هذا بشكل طبيعي `HEROKU_API_KEY` اذا كنت لاتعلم اين يوجد فقط اذهب الى حسابك في هيروكو ثم الى الاعدادات ستجده بالاسفل انسخه ودخله في الفار. ")

        if Config.HEROKU_APP_NAME is not None:
            app = Heroku.app(Config.HEROKU_APP_NAME)
        else:
            return await ed(event, "✾╎اضبط Var المطلوب في Heroku على وظيفة هذا بشكل طبيعي `HEROKU_APP_NAME` اسم التطبيق اذا كنت لاتعلم.")
        heroku_var = app.config()
        variable = "PRIVATE_CHANNEL_BOT_API_ID"
        await asyncio.sleep(1.5)
        if variable in heroku_var:
            await zed.edit("**✾╎تم تغييـر {} بنجـاح ☑️**\n**✾╎المتغيـر : ↶**\n `{}` \n**✾╎يتم الان اعـادة تشغيـل بـوت زد ثـون يستغـرق الامر 2-1 دقيقـه ▬▭ ...**".format(input_str, vinfo))
        else:
            await zed.edit("**✾╎تم اضافـة {} بنجـاح ☑️** \n**✾╎المضاف اليه :**\n `{}` \n**✾╎يتم الان اعـادة تشغيـل بـوت زد ثـون يستغـرق الامر 2-1 دقيقـه ▬▭ ...**".format(input_str, vinfo))
        heroku_var[variable] = vinfo
    elif input_str == "قناة الملفات" or input_str == "قناة الاضافات":
        if Config.HEROKU_API_KEY is None:
            return await ed(event, "✾╎اضبط Var المطلوب في Heroku على وظيفة هذا بشكل طبيعي `HEROKU_API_KEY` اذا كنت لاتعلم اين يوجد فقط اذهب الى حسابك في هيروكو ثم الى الاعدادات ستجده بالاسفل انسخه ودخله في الفار. ")

        if Config.HEROKU_APP_NAME is not None:
            app = Heroku.app(Config.HEROKU_APP_NAME)
        else:
            return await ed(event, "✾╎اضبط Var المطلوب في Heroku على وظيفة هذا بشكل طبيعي `HEROKU_APP_NAME` اسم التطبيق اذا كنت لاتعلم.")
        heroku_var = app.config()
        variable = "PLUGIN_CHANNEL"
        await asyncio.sleep(1.5)
        if variable in heroku_var:
            await zed.edit("**✾╎تم تغييـر {} بنجـاح ☑️**\n**✾╎المتغيـر : ↶**\n `{}` \n**✾╎يتم الان اعـادة تشغيـل بـوت زد ثـون يستغـرق الامر 2-1 دقيقـه ▬▭ ...**".format(input_str, vinfo))
        else:
            await zed.edit("**✾╎تم اضافـة {} بنجـاح ☑️** \n**✾╎المضاف اليه :**\n `{}` \n**✾╎يتم الان اعـادة تشغيـل بـوت زد ثـون يستغـرق الامر 2-1 دقيقـه ▬▭ ...**".format(input_str, vinfo))
        heroku_var[variable] = vinfo
    elif input_str == "ايديي" or input_str == "ايدي الحساب":
        if Config.HEROKU_API_KEY is None:
            return await ed(event, "✾╎اضبط Var المطلوب في Heroku على وظيفة هذا بشكل طبيعي `HEROKU_API_KEY` اذا كنت لاتعلم اين يوجد فقط اذهب الى حسابك في هيروكو ثم الى الاعدادات ستجده بالاسفل انسخه ودخله في الفار. ")

        if Config.HEROKU_APP_NAME is not None:
            app = Heroku.app(Config.HEROKU_APP_NAME)
        else:
            return await ed(event, "✾╎اضبط Var المطلوب في Heroku على وظيفة هذا بشكل طبيعي `HEROKU_APP_NAME` اسم التطبيق اذا كنت لاتعلم.")
        heroku_var = app.config()
        variable = "OWNER_ID"
        await asyncio.sleep(1.5)
        if variable in heroku_var:
            await zed.edit("**✾╎تم تغييـر {} بنجـاح ☑️**\n**✾╎المتغيـر : ↶**\n `{}` \n**✾╎يتم الان اعـادة تشغيـل بـوت زد ثـون يستغـرق الامر 2-1 دقيقـه ▬▭ ...**".format(input_str, vinfo))
        else:
            await zed.edit("**✾╎تم اضافـة {} بنجـاح ☑️** \n**✾╎المضاف اليه :**\n `{}` \n**✾╎يتم الان اعـادة تشغيـل بـوت زد ثـون يستغـرق الامر 2-1 دقيقـه ▬▭ ...**".format(input_str, vinfo))
        heroku_var[variable] = vinfo
    elif input_str == "نقطة الاوامر" or input_str == "نقطه الاوامر":
        if Config.HEROKU_API_KEY is None:
            return await ed(event, "✾╎اضبط Var المطلوب في Heroku على وظيفة هذا بشكل طبيعي `HEROKU_API_KEY` اذا كنت لاتعلم اين يوجد فقط اذهب الى حسابك في هيروكو ثم الى الاعدادات ستجده بالاسفل انسخه ودخله في الفار. ")

        if Config.HEROKU_APP_NAME is not None:
            app = Heroku.app(Config.HEROKU_APP_NAME)
        else:
            return await ed(event, "✾╎اضبط Var المطلوب في Heroku على وظيفة هذا بشكل طبيعي `HEROKU_APP_NAME` اسم التطبيق اذا كنت لاتعلم.")
        heroku_var = app.config()
        variable = "COMMAND_HAND_LER"
        await asyncio.sleep(1.5)
        if variable in heroku_var:
            await zed.edit("**✾╎تم تغييـر {} بنجـاح ☑️**\n**✾╎المتغيـر : ↶**\n `{}` \n**✾╎يتم الان اعـادة تشغيـل بـوت زد ثـون يستغـرق الامر 2-1 دقيقـه ▬▭ ...**".format(input_str, vinfo))
        else:
            await zed.edit("**✾╎تم اضافـة {} بنجـاح ☑️** \n**✾╎المضاف اليه :**\n `{}` \n**✾╎يتم الان اعـادة تشغيـل بـوت زد ثـون يستغـرق الامر 2-1 دقيقـه ▬▭ ...**".format(input_str, vinfo))
        heroku_var[variable] = vinfo
    elif input_str == "التوكن" or input_str == "توكن البوت":
        variable = "TG_BOT_TOKEN"
        await asyncio.sleep(1.5)
        if variable in heroku_var:
            await zed.edit("**✾╎تم تغييـر {} بنجـاح ☑️**\n**✾╎المتغيـر : ↶**\n `{}` \n**✾╎يتم الان اعـادة تشغيـل بـوت زد ثـون يستغـرق الامر 2-1 دقيقـه ▬▭ ...**".format(input_str, vinfo))
        else:
            await zed.edit("**✾╎تم اضافـة {} بنجـاح ☑️** \n**✾╎المضاف اليه :**\n `{}` \n**✾╎يتم الان اعـادة تشغيـل بـوت زد ثـون يستغـرق الامر 2-1 دقيقـه ▬▭ ...**".format(input_str, vinfo))
        heroku_var[variable] = vinfo
    elif input_str == "معرف البوت" or input_str == "معرف بوت":
        if Config.HEROKU_API_KEY is None:
            return await ed(event, "✾╎اضبط Var المطلوب في Heroku على وظيفة هذا بشكل طبيعي `HEROKU_API_KEY` اذا كنت لاتعلم اين يوجد فقط اذهب الى حسابك في هيروكو ثم الى الاعدادات ستجده بالاسفل انسخه ودخله في الفار. ")

        if Config.HEROKU_APP_NAME is not None:
            app = Heroku.app(Config.HEROKU_APP_NAME)
        else:
            return await ed(event, "✾╎اضبط Var المطلوب في Heroku على وظيفة هذا بشكل طبيعي `HEROKU_APP_NAME` اسم التطبيق اذا كنت لاتعلم.")
        heroku_var = app.config()
        variable = "TG_BOT_USERNAME"
        await asyncio.sleep(1.5)
        if variable in heroku_var:
            await zed.edit("**✾╎تم تغييـر {} بنجـاح ☑️**\n**✾╎المتغيـر : ↶**\n `{}` \n**✾╎يتم الان اعـادة تشغيـل بـوت زد ثـون يستغـرق الامر 2-1 دقيقـه ▬▭ ...**".format(input_str, vinfo))
        else:
            await zed.edit("**✾╎تم اضافـة {} بنجـاح ☑️** \n**✾╎المضاف اليه :**\n `{}` \n**✾╎يتم الان اعـادة تشغيـل بـوت زد ثـون يستغـرق الامر 2-1 دقيقـه ▬▭ ...**".format(input_str, vinfo))
        heroku_var[variable] = vinfo
    elif input_str == "الريبو" or input_str == "السورس":
        if Config.HEROKU_API_KEY is None:
            return await ed(event, "✾╎اضبط Var المطلوب في Heroku على وظيفة هذا بشكل طبيعي `HEROKU_API_KEY` اذا كنت لاتعلم اين يوجد فقط اذهب الى حسابك في هيروكو ثم الى الاعدادات ستجده بالاسفل انسخه ودخله في الفار. ")

        if Config.HEROKU_APP_NAME is not None:
            app = Heroku.app(Config.HEROKU_APP_NAME)
        else:
            return await ed(event, "✾╎اضبط Var المطلوب في Heroku على وظيفة هذا بشكل طبيعي `HEROKU_APP_NAME` اسم التطبيق اذا كنت لاتعلم.")
        heroku_var = app.config()
        variable = "UPSTREAM_REPO"
        await asyncio.sleep(1.5)
        if variable in heroku_var:
            await zed.edit("**✾╎تم تغييـر {} بنجـاح ☑️**\n**✾╎المتغيـر : ↶**\n `{}` \n**✾╎يتم الان اعـادة تشغيـل بـوت زد ثـون يستغـرق الامر 2-1 دقيقـه ▬▭ ...**".format(input_str, vinfo))
        else:
            await zed.edit("**✾╎تم اضافـة {} بنجـاح ☑️** \n**✾╎المضاف اليه :**\n `{}` \n**✾╎يتم الان اعـادة تشغيـل بـوت زد ثـون يستغـرق الامر 2-1 دقيقـه ▬▭ ...**".format(input_str, vinfo))
        heroku_var[variable] = vinfo
    elif input_str == "توكن المكافح" or input_str == "كود المكافح" or input_str == "مكافح التخريب" or input_str == "مكافح التفليش":
        if Config.HEROKU_API_KEY is None:
            return await ed(event, "✾╎اضبط Var المطلوب في Heroku على وظيفة هذا بشكل طبيعي `HEROKU_API_KEY` اذا كنت لاتعلم اين يوجد فقط اذهب الى حسابك في هيروكو ثم الى الاعدادات ستجده بالاسفل انسخه ودخله في الفار. ")

        if Config.HEROKU_APP_NAME is not None:
            app = Heroku.app(Config.HEROKU_APP_NAME)
        else:
            return await ed(event, "✾╎اضبط Var المطلوب في Heroku على وظيفة هذا بشكل طبيعي `HEROKU_APP_NAME` اسم التطبيق اذا كنت لاتعلم.")
        heroku_var = app.config()
        variable = "SPAMWATCH_API"
        await asyncio.sleep(1.5)
        if variable in heroku_var:
            await zed.edit("**✾╎تم تغييـر {} بنجـاح ☑️**\n**✾╎المتغيـر : ↶**\n `{}` \n**✾╎يتم الان اعـادة تشغيـل بـوت زد ثـون يستغـرق الامر 2-1 دقيقـه ▬▭ ...**".format(input_str, vinfo))
        else:
            await zed.edit("**✾╎تم اضافـة {} بنجـاح ☑️** \n**✾╎المضاف اليه :**\n `{}` \n**✾╎يتم الان اعـادة تشغيـل بـوت زد ثـون يستغـرق الامر 2-1 دقيقـه ▬▭ ...**".format(input_str, vinfo))
        heroku_var[variable] = vinfo
    else:
        if input_str:
            return await zed.edit("**✾╎عـذراً .. لايوجـد هنالك فـار بإسـم {} ؟!.. ارسـل (.اوامر الفارات) لـعرض قائمـة الفـارات**".format(input_str))

        return await edit_or_reply(event, "**✾╎عـذراً .. لايوجـد هنالك فـار بإسـم {} ؟!.. ارسـل (.اوامر الفارات) لـعرض قائمـة الفـارات**".format(input_str))



# Copyright (C) 2022 Zed-Thon . All Rights Reserved
@zedub.zed_cmd(pattern="حذف(?:\s|$)([\s\S]*)")
async def variable(event):
    if Config.HEROKU_API_KEY is None:
        return await ed(
            event,
            "✾╎اضبط Var المطلوب في Heroku على وظيفة هذا بشكل طبيعي `HEROKU_API_KEY` اذا كنت لاتعلم اين يوجد فقط اذهب الى حسابك في هيروكو ثم الى الاعدادات ستجده بالاسفل انسخه ودخله في الفار. ",
        )
    if Config.HEROKU_APP_NAME is not None:
        app = Heroku.app(Config.HEROKU_APP_NAME)
    else:
        return await ed(
            event,
            "✾╎اضبط Var المطلوب في Heroku على وظيفة هذا بشكل طبيعي `HEROKU_APP_NAME` اسم التطبيق اذا كنت لاتعلم.",
        )
    input_str = event.text[5:]
    heroku_var = app.config()
    zed = await edit_or_reply(event, "**✾╎جـاري حـذف الفـار مـن بـوتك 🚮...**")
    # All Rights Reserved for "Zed-Thon" "زلـزال الهيبـه"
    if input_str == "كليشة الفحص" or input_str == "كليشه الفحص":
        variable = "ALIVE_TEMPLATE"
        await asyncio.sleep(1.5)
        if gvarstatus("ALIVE_TEMPLATE") is None:
        	return await zed.edit("**✾╎عـذراً عـزيـزي .. انت لـم تقـم باضـافـة فـار {} اصـلاً...**".format(input_str))
        await zed.edit("**✾╎تم حـذف {} بنجـاح ☑️**\n**✾╎المتغيـر المحـذوف : ↶**\n `{}` \n**✾╎يتم الان اعـادة تشغيـل بـوت زد ثـون يستغـرق الامر 2-1 دقيقـه ▬▭ ...**".format(input_str, heroku_var[variable]))
        delgvar("ALIVE_TEMPLATE")
        
    elif input_str == "كليشة الحماية" or input_str == "كليشه الحمايه" or input_str == "كليشه الحماية" or input_str == "كليشة الحمايه":
        variable = "pmpermit_txt"
        await asyncio.sleep(1.5)
        if gvarstatus("pmpermit_txt") is None:
        	return await zed.edit("**✾╎عـذراً عـزيـزي .. انت لـم تقـم باضـافـة فـار {} اصـلاً...**".format(input_str))
        await zed.edit("**✾╎تم حـذف {} بنجـاح ☑️**\n**✾╎المتغيـر المحـذوف : ↶**\n `{}` \n**✾╎يتم الان اعـادة تشغيـل بـوت زد ثـون يستغـرق الامر 2-1 دقيقـه ▬▭ ...**".format(input_str, heroku_var[variable]))
        delgvar("pmpermit_txt")

    elif input_str == "كليشة البوت" or input_str == "كليشه البوت":
        variable = "START_TEXT"
        await asyncio.sleep(1.5)
        if gvarstatus("START_TEXT") is None:
        	return await zed.edit("**✾╎عـذراً عـزيـزي .. انت لـم تقـم باضـافـة فـار {} اصـلاً...**".format(input_str))
        await zed.edit("**✾╎تم حـذف {} بنجـاح ☑️**\n**✾╎المتغيـر المحـذوف : ↶**\n `{}` \n**✾╎يتم الان اعـادة تشغيـل بـوت زد ثـون يستغـرق الامر 2-1 دقيقـه ▬▭ ...**".format(input_str, heroku_var[variable]))
        delgvar("START_TEXT")

    elif input_str == "كليشة الحظر" or input_str == "كليشه الحظر":
        variable = "pmblock"
        await asyncio.sleep(1.5)
        if gvarstatus("pmblock") is None:
        	return await zed.edit("**✾╎عـذراً عـزيـزي .. انت لـم تقـم باضـافـة فـار {} اصـلاً...**".format(input_str))
        await zed.edit("**✾╎تم حـذف {} بنجـاح ☑️**\n**✾╎المتغيـر المحـذوف : ↶**\n `{}` \n**✾╎يتم الان اعـادة تشغيـل بـوت زد ثـون يستغـرق الامر 2-1 دقيقـه ▬▭ ...**".format(input_str, heroku_var[variable]))
        delgvar("pmblock")

    elif input_str == "صورة الفحص" or input_str == "صوره الفحص":
        variable = "ALIVE_PIC"
        await asyncio.sleep(1.5)
        if gvarstatus("ALIVE_PIC") is None:
        	return await zed.edit("**✾╎عـذراً عـزيـزي .. انت لـم تقـم باضـافـة فـار {} اصـلاً...**".format(input_str))
        await zed.edit("**✾╎تم حـذف فـار {} . . بنجـاح ☑️**".format(input_str))
        delgvar("ALIVE_PIC")

    elif input_str == "صورة الاوامر" or input_str == "صوره الاوامر":
        variable = "CMD_PIC"
        await asyncio.sleep(1.5)
        if gvarstatus("CMD_PIC") is None:
        	return await zed.edit("**✾╎عـذراً عـزيـزي .. انت لـم تقـم باضـافـة فـار {} اصـلاً...**".format(input_str))
        await zed.edit("**✾╎تم حـذف فـار {} . . بنجـاح ☑️**".format(input_str))
        delgvar("CMD_PIC")

    elif input_str == "صورة السورس" or input_str == "صوره السورس":
        variable = "ALIVE_PIC"
        await asyncio.sleep(1.5)
        if gvarstatus("ALIVE_PIC") is None:
        	return await zed.edit("**✾╎عـذراً عـزيـزي .. انت لـم تقـم باضـافـة فـار {} اصـلاً...**".format(input_str))
        await zed.edit("**✾╎تم حـذف فـار {} . . بنجـاح ☑️**".format(input_str))
        delgvar("ALIVE_PIC")

    elif input_str == "صورة الكتم" or input_str == "صوره الكتم":
        variable = "KTM_PIC"
        await asyncio.sleep(1.5)
        if gvarstatus("KTM_PIC") is None:
        	return await zed.edit("**✾╎عـذراً عـزيـزي .. انت لـم تقـم باضـافـة فـار {} اصـلاً...**".format(input_str))
        await zed.edit("**✾╎تم حـذف فـار {} . . بنجـاح ☑️**".format(input_str))
        delgvar("KTM_PIC")

    elif input_str == "صورة البوت" or input_str == "صوره البوت":
        variable = "BOT_START_PIC"
        await asyncio.sleep(1.5)
        if gvarstatus("BOT_START_PIC") is None:
        	return await zed.edit("**✾╎عـذراً عـزيـزي .. انت لـم تقـم باضـافـة فـار {} اصـلاً...**".format(input_str))
        await zed.edit("**✾╎تم حـذف فـار {} . . بنجـاح ☑️**".format(input_str))
        delgvar("BOT_START_PIC")

    elif input_str == "صورة الحماية" or input_str == "صوره الحمايه" or input_str == "صورة الحمايه" or input_str == "صوره الحماية":
        variable = "pmpermit_pic"
        await asyncio.sleep(1.5)
        if gvarstatus("pmpermit_pic") is None:
        	return await zed.edit("**✾╎عـذراً عـزيـزي .. انت لـم تقـم باضـافـة فـار {} اصـلاً...**".format(input_str))
        delgvar("pmpermit_pic")
        await zed.edit("**✾╎تم حـذف فـار {} . . بنجـاح ☑️**".format(input_str))

    elif input_str == "صورة الوقتي" or input_str == "صوره الوقتي":
        variable = "DIGITAL_PIC"
        await asyncio.sleep(1.5)
        if gvarstatus("DIGITAL_PIC") is None:
        	return await zed.edit("**✾╎عـذراً عـزيـزي .. انت لـم تقـم باضـافـة فـار {} اصـلاً...**".format(input_str))
        await zed.edit("**✾╎تم حـذف {} بنجـاح ☑️**\n**✾╎المتغيـر المحـذوف : ↶**\n `{}` \n**✾╎يتم الان اعـادة تشغيـل بـوت زد ثـون يستغـرق الامر 2-1 دقيقـه ▬▭ ...**".format(input_str, heroku_var[variable]))
        delgvar("DIGITAL_PIC")

    elif input_str == "رمز الوقتي" or input_str == "رمز الاسم الوقتي":
        variable = "CUSTOM_ALIVE_EMZED"
        await asyncio.sleep(1.5)
        if gvarstatus("CUSTOM_ALIVE_EMZED") is None:
        	return await zed.edit("**✾╎عـذراً عـزيـزي .. انت لـم تقـم باضـافـة فـار {} اصـلاً...**".format(input_str))
        delgvar("CUSTOM_ALIVE_EMZED")
        await zed.edit("**✾╎تم حـذف فـار {} . . بنجـاح ☑️**".format(input_str))
    elif input_str == "زخرفه الوقتي" or input_str == "زخرفة الوقتي":
        variable = "ZI_FN"
        await asyncio.sleep(1.5)
        if variable not in heroku_var:
        	return await zed.edit("**✾╎عـذراً عـزيـزي .. انت لـم تقـم باضـافـة فـار {} اصـلاً...**".format(input_str))
        await zed.edit("**✾╎تم حـذف {} بنجـاح ☑️**\n**✾╎المتغيـر المحـذوف : ↶**\n `{}` \n**✾╎يتم الان اعـادة تشغيـل بـوت زد ثـون يستغـرق الامر 2-1 دقيقـه ▬▭ ...**".format(input_str, heroku_var[variable]))
        del heroku_var[variable]
    elif input_str == "البايو" or input_str == "البايو الوقتي" or input_str == "النبذه الوقتيه":
        variable = "DEFAULT_BIO"
        await asyncio.sleep(1.5)
        if gvarstatus("DEFAULT_BIO") is None:
        	return await zed.edit("**✾╎عـذراً عـزيـزي .. انت لـم تقـم باضـافـة فـار {} اصـلاً...**".format(input_str))
        delgvar("DEFAULT_BIO")
        await zed.edit("**✾╎تم حـذف فـار {} . . بنجـاح ☑️**".format(input_str))
    elif input_str == "اسم المستخدم" or input_str == "الاسم":
        variable = "ALIVE_NAME"
        await asyncio.sleep(1.5)
        if variable not in heroku_var:
        	return await zed.edit("**✾╎عـذراً عـزيـزي .. انت لـم تقـم باضـافـة فـار {} اصـلاً...**".format(input_str))
        await zed.edit("**✾╎تم حـذف {} بنجـاح ☑️**\n**✾╎المتغيـر المحـذوف : ↶**\n `{}` \n**✾╎يتم الان اعـادة تشغيـل بـوت زد ثـون يستغـرق الامر 2-1 دقيقـه ▬▭ ...**".format(input_str, heroku_var[variable]))
        del heroku_var[variable]
    elif input_str == "كروب الرسائل" or input_str == "كروب التخزين" or input_str == "كروب الخاص":
        variable = "PM_LOGGER_GROUP_ID"
        await asyncio.sleep(1.5)
        if variable not in heroku_var:
        	return await zed.edit("**✾╎عـذراً عـزيـزي .. انت لـم تقـم باضـافـة فـار {} اصـلاً...**".format(input_str))
        await zed.edit("**✾╎تم حـذف {} بنجـاح ☑️**\n**✾╎المتغيـر المحـذوف : ↶**\n `{}` \n**✾╎يتم الان اعـادة تشغيـل بـوت زد ثـون يستغـرق الامر 2-1 دقيقـه ▬▭ ...**".format(input_str, heroku_var[variable]))
        del heroku_var[variable]

    elif input_str == "السجل" or input_str == "كروب السجل":
        variable = "PRIVATE_GROUP_BOT_API_ID"
        await asyncio.sleep(1.5)
        if variable not in heroku_var:
        	return await zed.edit("**✾╎عـذراً عـزيـزي .. انت لـم تقـم باضـافـة فـار {} اصـلاً...**".format(input_str))
        await zed.edit("**✾╎تم حـذف {} بنجـاح ☑️**\n**✾╎المتغيـر المحـذوف : ↶**\n `{}` \n**✾╎يتم الان اعـادة تشغيـل بـوت زد ثـون يستغـرق الامر 2-1 دقيقـه ▬▭ ...**".format(input_str, heroku_var[variable]))
        del heroku_var[variable]

    elif input_str == "السجل 2" or input_str == "كروب السجل 2":
        variable = "PRIVATE_GROUP_ID"
        await asyncio.sleep(1.5)
        if variable not in heroku_var:
        	return await zed.edit("**✾╎عـذراً عـزيـزي .. انت لـم تقـم باضـافـة فـار {} اصـلاً...**".format(input_str))
        await zed.edit("**✾╎تم حـذف {} بنجـاح ☑️**\n**✾╎المتغيـر المحـذوف : ↶**\n `{}` \n**✾╎يتم الان اعـادة تشغيـل بـوت زد ثـون يستغـرق الامر 2-1 دقيقـه ▬▭ ...**".format(input_str, heroku_var[variable]))
        del heroku_var[variable]

    elif input_str == "قناة السجل" or input_str == "قناة السجلات":
        variable = "PRIVATE_CHANNEL_BOT_API_ID"
        await asyncio.sleep(1.5)
        if variable not in heroku_var:
        	return await zed.edit("**✾╎عـذراً عـزيـزي .. انت لـم تقـم باضـافـة فـار {} اصـلاً...**".format(input_str))
        await zed.edit("**✾╎تم حـذف {} بنجـاح ☑️**\n**✾╎المتغيـر المحـذوف : ↶**\n `{}` \n**✾╎يتم الان اعـادة تشغيـل بـوت زد ثـون يستغـرق الامر 2-1 دقيقـه ▬▭ ...**".format(input_str, heroku_var[variable]))
        del heroku_var[variable]

    elif input_str == "قناة الملفات" or input_str == "قناة الاضافات":
        variable = "PLUGIN_CHANNEL"
        await asyncio.sleep(1.5)
        if variable not in heroku_var:
        	return await zed.edit("**✾╎عـذراً عـزيـزي .. انت لـم تقـم باضـافـة فـار {} اصـلاً...**".format(input_str))
        await zed.edit("**✾╎تم حـذف {} بنجـاح ☑️**\n**✾╎المتغيـر المحـذوف : ↶**\n `{}` \n**✾╎يتم الان اعـادة تشغيـل بـوت زد ثـون يستغـرق الامر 2-1 دقيقـه ▬▭ ...**".format(input_str, heroku_var[variable]))
        del heroku_var[variable]

    elif input_str == "ايديي" or input_str == "ايدي الحساب":
        variable = "OWNER_ID"
        await asyncio.sleep(1.5)
        if variable not in heroku_var:
        	return await zed.edit("**✾╎عـذراً عـزيـزي .. انت لـم تقـم باضـافـة فـار {} اصـلاً...**".format(input_str))
        await zed.edit("**✾╎تم حـذف {} بنجـاح ☑️**\n**✾╎المتغيـر المحـذوف : ↶**\n `{}` \n**✾╎يتم الان اعـادة تشغيـل بـوت زد ثـون يستغـرق الامر 2-1 دقيقـه ▬▭ ...**".format(input_str, heroku_var[variable]))
        del heroku_var[variable]

    elif input_str == "نقطة الاوامر" or input_str == "نقطه الاوامر":
        variable = "COMMAND_HAND_LER"
        await asyncio.sleep(1.5)
        if variable not in heroku_var:
        	return await zed.edit("**✾╎عـذراً عـزيـزي .. انت لـم تقـم باضـافـة فـار {} اصـلاً...**".format(input_str))
        await zed.edit("**✾╎تم حـذف {} بنجـاح ☑️**\n**✾╎المتغيـر المحـذوف : ↶**\n `{}` \n**✾╎يتم الان اعـادة تشغيـل بـوت زد ثـون يستغـرق الامر 2-1 دقيقـه ▬▭ ...**".format(input_str, heroku_var[variable]))
        del heroku_var[variable]

    elif input_str == "التوكن" or input_str == "توكن البوت":
        variable = "TG_BOT_TOKEN"
        await asyncio.sleep(1.5)
        if variable not in heroku_var:
        	return await zed.edit("**✾╎عـذراً عـزيـزي .. انت لـم تقـم باضـافـة فـار {} اصـلاً...**".format(input_str))
        await zed.edit("**✾╎تم حـذف {} بنجـاح ☑️**\n**✾╎المتغيـر المحـذوف : ↶**\n `{}` \n**✾╎يتم الان اعـادة تشغيـل بـوت زد ثـون يستغـرق الامر 2-1 دقيقـه ▬▭ ...**".format(input_str, heroku_var[variable]))
        del heroku_var[variable]

    elif input_str == "معرف البوت" or input_str == "معرف بوت":
        variable = "TG_BOT_USERNAME"
        await asyncio.sleep(1.5)
        if variable not in heroku_var:
        	return await zed.edit("**✾╎عـذراً عـزيـزي .. انت لـم تقـم باضـافـة فـار {} اصـلاً...**".format(input_str))
        await zed.edit("**✾╎تم حـذف {} بنجـاح ☑️**\n**✾╎المتغيـر المحـذوف : ↶**\n `{}` \n**✾╎يتم الان اعـادة تشغيـل بـوت زد ثـون يستغـرق الامر 2-1 دقيقـه ▬▭ ...**".format(input_str, heroku_var[variable]))
        del heroku_var[variable]

    elif input_str == "الريبو" or input_str == "السورس":
        variable = "UPSTREAM_REPO"
        await asyncio.sleep(1.5)
        if variable not in heroku_var:
        	return await zed.edit("**✾╎عـذراً عـزيـزي .. انت لـم تقـم باضـافـة فـار {} اصـلاً...**".format(input_str))
        await zed.edit("**✾╎تم حـذف {} بنجـاح ☑️**\n**✾╎المتغيـر المحـذوف : ↶**\n `{}` \n**✾╎يتم الان اعـادة تشغيـل بـوت زد ثـون يستغـرق الامر 2-1 دقيقـه ▬▭ ...**".format(input_str, heroku_var[variable]))
        del heroku_var[variable]

    elif input_str == "اسمي التلقائي" or input_str == "الاسم التلقاائي":
        variable = "AUTONAME"
        await asyncio.sleep(1.5)
        if variable not in heroku_var:
        	return await zed.edit("**✾╎عـذراً عـزيـزي .. انت لـم تقـم باضـافـة فـار {} اصـلاً...**".format(input_str))
        await zed.edit("**✾╎تم حـذف {} بنجـاح ☑️**\n**✾╎المتغيـر المحـذوف : ↶**\n `{}` \n**✾╎يتم الان اعـادة تشغيـل بـوت زد ثـون يستغـرق الامر 2-1 دقيقـه ▬▭ ...**".format(input_str, heroku_var[variable]))
        del heroku_var[variable]
    elif input_str == "رسائل الحماية" or input_str == "رسائل الحمايه" or input_str == "رسائل الخاص" or input_str == "رسائل حماية الخاص" or input_str == "عدد التحذيرات":
        variable = gvarstatus("MAX_FLOOD_IN_PMS")
        await asyncio.sleep(1.5)
        if variable is None:
        	return await zed.edit("**✾╎عـذراً عـزيـزي .. انت لـم تقـم باضـافـة فـار {} اصـلاً...**".format(input_str))
        await zed.edit("**✾╎تم حـذف {} بنجـاح ☑️**\n**✾╎المتغيـر المحـذوف : ↶**\n `{}`".format(input_str, variable))
        delgvar("MAX_FLOOD_IN_PMS")
    elif input_str == "ايموجي الايدي" or input_str == "ايموجي ايدي" or input_str == "رمز الايدي" or input_str == "رمز ايدي" or input_str == "الرمز ايدي":
        variable = gvarstatus("CUSTOM_ALIVE_EMOJI")
        await asyncio.sleep(1.5)
        if variable is None:
        	return await zed.edit("**✾╎عـذراً عـزيـزي .. انت لـم تقـم باضـافـة فـار {} اصـلاً...**".format(input_str))
        await zed.edit("**✾╎تم حـذف {} بنجـاح ☑️**\n**✾╎المتغيـر المحـذوف : ↶**\n `{}`".format(input_str, variable))
        delgvar("CUSTOM_ALIVE_EMOJI")
    elif input_str == "عنوان الايدي" or input_str == "عنوان ايدي":
        variable = gvarstatus("CUSTOM_ALIVE_TEXT")
        await asyncio.sleep(1.5)
        if variable is None:
        	return await zed.edit("**✾╎عـذراً عـزيـزي .. انت لـم تقـم باضـافـة فـار {} اصـلاً...**".format(input_str))
        await zed.edit("**✾╎تم حـذف {} بنجـاح ☑️**\n**✾╎المتغيـر المحـذوف : ↶**\n `{}`".format(input_str, variable))
        delgvar("CUSTOM_ALIVE_TEXT")
    elif input_str == "خط الايدي" or input_str == "خط ايدي" or input_str == "خطوط الايدي" or input_str == "خط ايدي":
        variable = gvarstatus("CUSTOM_ALIVE_FONT")
        await asyncio.sleep(1.5)
        if variable is None:
        	return await zed.edit("**✾╎عـذراً عـزيـزي .. انت لـم تقـم باضـافـة فـار {} اصـلاً...**".format(input_str))
        await zed.edit("**✾╎تم حـذف {} بنجـاح ☑️**\n**✾╎المتغيـر المحـذوف : ↶**\n `{}`".format(input_str, variable))
        delgvar("CUSTOM_ALIVE_FONT")
    else:
        if input_str:
            return await zed.edit("**✾╎عـذراً .. لايوجـد هنالك فـار بإسـم {} ؟!.. ارسـل (.اوامر الفارات) لـعرض قائمـة الفـارات**".format(input_str))
        return await edit_or_reply(event, "**✾╎عـذراً .. لايوجـد هنالك فـار بإسـم {} ؟!.. ارسـل (.اوامر الفارات) لـعرض قائمـة الفـارات**".format(input_str))


# Copyright (C) 2022 Zed-Thon . All Rights Reserved
@zedub.zed_cmd(pattern="جلب(?:\s|$)([\s\S]*)")
async def custom_zed(event):
    input_str = event.text[5:]
    zed = await edit_or_reply(event, "**✾╎جــاري جلـب معلـومـات الفــار 🛂. . .**")
    if (input_str == "كليشة الحماية" or input_str == "كليشة الحمايه" or input_str == "كليشه الحماية" or input_str == "كليشه الحمايه"):
        variable = gvarstatus("pmpermit_txt")
        if variable is None:
            await zed.edit("**✾╎فـار كليشـة الحمايـة غيـر موجـود ❌**\n**✾╎لـ اضـافته بالـرد ع الكليشـة استخـدم الامـر : ↶**\n `.اضف كليشة الحماية` \n\n**✾╎قنـاة السـورس : @ZEDThon**")
        else:
            await zed.edit("**✾╎الفـار {} موجـود ☑️**\n**✾╎قيمـة الفـار : ↶**\n `{}` \n\n**✾╎قنـاة السـورس : @ZEDThon**".format(input_str, variable))
            
    elif input_str == "كليشة الفحص" or input_str == "كليشه الفحص":
        variable = gvarstatus("ALIVE_TEMPLATE")
        if variable is None:
            await zed.edit("**✾╎فـار كليشـة الفحص غيـر موجـود ❌**\n**✾╎لـ اضـافته بالـرد ع الكليشـة استخـدم الامـر : ↶**\n `.اضف كليشة الفحص` \n\n**✾╎قنـاة السـورس : @ZEDThon**")
        else:
            await zed.edit("**✾╎الفـار {} موجـود ☑️**\n**✾╎قيمـة الفـار : ↶**\n `{}` \n\n**✾╎قنـاة السـورس : @ZEDThon**".format(input_str, variable))

    elif input_str == "كليشة البوت" or input_str == "كليشه البوت":
        variable = gvarstatus("START_TEXT")
        if variable is None:
            await zed.edit("**✾╎فـار كليشـة البـوت غيـر موجـود ❌**\n**✾╎لـ اضـافته بالـرد ع الكليشـة استخـدم الامـر : ↶**\n `.اضف كليشة البوت` \n\n**✾╎قنـاة السـورس : @ZEDThon**")
        else:
            await zed.edit("**✾╎الفـار {} موجـود ☑️**\n**✾╎قيمـة الفـار : ↶**\n `{}` \n\n**✾╎قنـاة السـورس : @ZEDThon**".format(input_str, variable))

    elif input_str == "كليشة الحظر" or input_str == "كليشه الحظر":
        variable = gvarstatus("pmblock")
        if variable is None:
            await zed.edit("**✾╎فـار كليشـة الحظـر غيـر موجـود ❌**\n**✾╎لـ اضـافته بالـرد ع الكليشـة استخـدم الامـر : ↶**\n `.اضف كليشة الحظر` \n\n**✾╎قنـاة السـورس : @ZEDThon**")
        else:
            await zed.edit("**✾╎الفـار {} موجـود ☑️**\n**✾╎قيمـة الفـار : ↶**\n `{}` \n\n**✾╎قنـاة السـورس : @ZEDThon**".format(input_str, variable))

    elif input_str == "رمز الوقتي" or input_str == "رمز الاسم الوقتي":
        variable = gvarstatus("CUSTOM_ALIVE_EMZED")
        if variable is None:
            await zed.edit("**✾╎فـار رمـز الوقتـي غيـر موجـود ❌**\n**✾╎لـ اضـافته بالـرد ع الرمـز استخـدم الامـر : ↶**\n `.اضف رمز الوقتي` \n\n**✾╎قنـاة السـورس : @ZEDThon**")
        else:
            await zed.edit("**✾╎الفـار {} موجـود ☑️**\n**✾╎قيمـة الفـار : ↶**\n `{}` \n\n**✾╎قنـاة السـورس : @ZEDThon**".format(input_str, variable))

    elif input_str == "كاشف الاباحي" or input_str == "كشف الاباحي":
        variable = gvarstatus("DEEP_API")
        if variable is None:
            await zed.edit("**✾╎فـار كشـف الاباحي غيـر موجـود ❌**\n**✾╎لـ اضـافته بالـرد ع الكـود استخـدم الامـر : ↶**\n `.اضف كاشف الاباحي` \n\n**✾╎قنـاة السـورس : @ZEDThon**")
        else:
            await zed.edit("**✾╎الفـار {} موجـود ☑️**\n**✾╎قيمـة الفـار : ↶**\n `{}` \n\n**✾╎قنـاة السـورس : @ZEDThon**".format(input_str, variable))

    elif input_str == "البايو" or input_str == "البايو الوقتي" or input_str == "النبذه" or input_str == "البايو تلقائي":
        variable = gvarstatus("DEFAULT_BIO")
        if variable is None:
            await zed.edit("**✾╎فـار البايـو الوقتـي غيـر موجـود ❌**\n**✾╎لـ اضـافته بالـرد ع نـص استخـدم الامـر : ↶**\n `.اضف البايو` \n\n**✾╎قنـاة السـورس : @ZEDThon**")
        else:
            await zed.edit("**✾╎الفـار {} موجـود ☑️**\n**✾╎قيمـة الفـار : ↶**\n `{}` \n\n**✾╎قنـاة السـورس : @ZEDThon**".format(input_str, variable))

    elif input_str == "اسم المستخدم" or input_str == "الاسم":
        if Config.HEROKU_API_KEY is None:
            return await ed(event, "✾╎اضبط Var المطلوب في Heroku على وظيفة هذا بشكل طبيعي `HEROKU_API_KEY` اذا كنت لاتعلم اين يوجد فقط اذهب الى حسابك في هيروكو ثم الى الاعدادات ستجده بالاسفل انسخه ودخله في الفار. ")
        if Config.HEROKU_APP_NAME is not None:
            app = Heroku.app(Config.HEROKU_APP_NAME)
        else:
            return await ed(event, "✾╎اضبط Var المطلوب في Heroku على وظيفة هذا بشكل طبيعي `HEROKU_APP_NAME` اسم التطبيق اذا كنت لاتعلم.")
        heroku_var = app.config()
        variable = "ALIVE_NAME"
        if variable not in heroku_var:
            await zed.edit("**✾╎فـار اسـم المستخـدم غيـر موجـود ❌**\n**✾╎لـ اضـافته بالـرد ع الاسم استخـدم الامـر : ↶**\n `.اضف اسم المستخدم` \n\n**✾╎قنـاة السـورس : @ZEDThon**")
        else:
            await zed.edit("**✾╎الفـار {} موجـود ☑️**\n**✾╎قيمـة الفـار : ↶**\n `{}` \n\n**✾╎قنـاة السـورس : @ZEDThon**".format(input_str, variable))

    elif input_str == "ايديي" or input_str == "ايدي الحساب":
        if Config.HEROKU_API_KEY is None:
            return await ed(event, "✾╎اضبط Var المطلوب في Heroku على وظيفة هذا بشكل طبيعي `HEROKU_API_KEY` اذا كنت لاتعلم اين يوجد فقط اذهب الى حسابك في هيروكو ثم الى الاعدادات ستجده بالاسفل انسخه ودخله في الفار. ")
        if Config.HEROKU_APP_NAME is not None:
            app = Heroku.app(Config.HEROKU_APP_NAME)
        else:
            return await ed(event, "✾╎اضبط Var المطلوب في Heroku على وظيفة هذا بشكل طبيعي `HEROKU_APP_NAME` اسم التطبيق اذا كنت لاتعلم.")
        heroku_var = app.config()
        variable = "OWNER_ID"
        if variable not in heroku_var:
            await zed.edit("**✾╎فـار ايـدي الحسـاب غيـر موجـود ❌**\n**✾╎لـ اضـافته بالـرد ع الايـدي فقـط استخـدم الامـر : ↶**\n `.اضف ايدي الحساب` \n\n**✾╎قنـاة السـورس : @ZEDThon**")
        else:
            await zed.edit("**✾╎الفـار {} موجـود ☑️**\n**✾╎قيمـة الفـار : ↶**\n `{}` \n\n**✾╎قنـاة السـورس : @ZEDThon**".format(input_str, variable))

    elif input_str == "نقطة الاوامر" or input_str == "نقطه الاوامر":
        if Config.HEROKU_API_KEY is None:
            return await ed(event, "✾╎اضبط Var المطلوب في Heroku على وظيفة هذا بشكل طبيعي `HEROKU_API_KEY` اذا كنت لاتعلم اين يوجد فقط اذهب الى حسابك في هيروكو ثم الى الاعدادات ستجده بالاسفل انسخه ودخله في الفار. ")
        if Config.HEROKU_APP_NAME is not None:
            app = Heroku.app(Config.HEROKU_APP_NAME)
        else:
            return await ed(event, "✾╎اضبط Var المطلوب في Heroku على وظيفة هذا بشكل طبيعي `HEROKU_APP_NAME` اسم التطبيق اذا كنت لاتعلم.")
        heroku_var = app.config()
        variable = "COMMAND_HAND_LER"
        if variable not in heroku_var:
            await zed.edit("**✾╎فـار نقطـة الاوامـر غيـر موجـود ❌**\n**✾╎لـ اضـافته بالـرد ع الرمـز فقـط استخـدم الامـر : ↶**\n `.اضف نقطة الاوامر` \n\n**✾╎قنـاة السـورس : @ZEDThon**")
        else:
            await zed.edit("**✾╎الفـار {} موجـود ☑️**\n**✾╎قيمـة الفـار : ↶**\n `{}` \n\n**✾╎قنـاة السـورس : @ZEDThon**".format(input_str, variable))

    elif input_str == "التوكن" or input_str == "توكن البوت":
        if Config.HEROKU_API_KEY is None:
            return await ed(event, "✾╎اضبط Var المطلوب في Heroku على وظيفة هذا بشكل طبيعي `HEROKU_API_KEY` اذا كنت لاتعلم اين يوجد فقط اذهب الى حسابك في هيروكو ثم الى الاعدادات ستجده بالاسفل انسخه ودخله في الفار. ")
        if Config.HEROKU_APP_NAME is not None:
            app = Heroku.app(Config.HEROKU_APP_NAME)
        else:
            return await ed(event, "✾╎اضبط Var المطلوب في Heroku على وظيفة هذا بشكل طبيعي `HEROKU_APP_NAME` اسم التطبيق اذا كنت لاتعلم.")
        heroku_var = app.config()
        variable = "TG_BOT_TOKEN"
        if variable not in heroku_var:
            await zed.edit("**✾╎فـار توكـن البـوت غيـر موجـود ❌**\n**✾╎لـ اضـافته بالـرد ع التوكـن فقـط استخـدم الامـر : ↶**\n `.اضف التوكن` \n\n**✾╎قنـاة السـورس : @ZEDThon**")
        else:
            await zed.edit("**✾╎الفـار {} موجـود ☑️**\n**✾╎قيمـة الفـار : ↶**\n `{}` \n\n**✾╎قنـاة السـورس : @ZEDThon**".format(input_str, variable))

    elif input_str == "معرف البوت" or input_str == "معرف بوت":
        if Config.HEROKU_API_KEY is None:
            return await ed(event, "✾╎اضبط Var المطلوب في Heroku على وظيفة هذا بشكل طبيعي `HEROKU_API_KEY` اذا كنت لاتعلم اين يوجد فقط اذهب الى حسابك في هيروكو ثم الى الاعدادات ستجده بالاسفل انسخه ودخله في الفار. ")
        if Config.HEROKU_APP_NAME is not None:
            app = Heroku.app(Config.HEROKU_APP_NAME)
        else:
            return await ed(event, "✾╎اضبط Var المطلوب في Heroku على وظيفة هذا بشكل طبيعي `HEROKU_APP_NAME` اسم التطبيق اذا كنت لاتعلم.")
        heroku_var = app.config()
        variable = "TG_BOT_USERNAME"
        if variable not in heroku_var:
            await zed.edit("**✾╎فـار معرف البوت غيـر موجـود ❌**\n**✾╎لـ اضـافته بالـرد ع المعرف استخـدم الامـر : ↶**\n `.اضف معرف البوت` \n\n**✾╎قنـاة السـورس : @ZEDThon**")
        else:
            await zed.edit("**✾╎الفـار {} موجـود ☑️**\n**✾╎قيمـة الفـار : ↶**\n `{}` \n\n**✾╎قنـاة السـورس : @ZEDThon**".format(input_str, variable))

    elif input_str == "الريبو" or input_str == "السورس":
        if Config.HEROKU_API_KEY is None:
            return await ed(event, "✾╎اضبط Var المطلوب في Heroku على وظيفة هذا بشكل طبيعي `HEROKU_API_KEY` اذا كنت لاتعلم اين يوجد فقط اذهب الى حسابك في هيروكو ثم الى الاعدادات ستجده بالاسفل انسخه ودخله في الفار. ")
        if Config.HEROKU_APP_NAME is not None:
            app = Heroku.app(Config.HEROKU_APP_NAME)
        else:
            return await ed(event, "✾╎اضبط Var المطلوب في Heroku على وظيفة هذا بشكل طبيعي `HEROKU_APP_NAME` اسم التطبيق اذا كنت لاتعلم.")
        heroku_var = app.config()
        variable = "UPSTREAM_REPO"
        if variable not in heroku_var:
            await zed.edit("**✾╎فـار الريبـو غيـر موجـود ❌**\n**✾╎لـ اضـافته بالـرد ع رابط السورس الرسمي استخـدم الامـر : ↶**\n `.اضف الريبو` \n\n**✾╎قنـاة السـورس : @ZEDThon**")
        else:
            await zed.edit("**✾╎الفـار {} موجـود ☑️**\n**✾╎قيمـة الفـار : ↶**\n `{}` \n\n**✾╎قنـاة السـورس : @ZEDThon**".format(input_str, variable))

    elif input_str == "اسمي التلقائي" or input_str == "الاسم التلقاائي":
        if Config.HEROKU_API_KEY is None:
            return await ed(event, "✾╎اضبط Var المطلوب في Heroku على وظيفة هذا بشكل طبيعي `HEROKU_API_KEY` اذا كنت لاتعلم اين يوجد فقط اذهب الى حسابك في هيروكو ثم الى الاعدادات ستجده بالاسفل انسخه ودخله في الفار. ")
        if Config.HEROKU_APP_NAME is not None:
            app = Heroku.app(Config.HEROKU_APP_NAME)
        else:
            return await ed(event, "✾╎اضبط Var المطلوب في Heroku على وظيفة هذا بشكل طبيعي `HEROKU_APP_NAME` اسم التطبيق اذا كنت لاتعلم.")
        heroku_var = app.config()
        variable = "AUTONAME"
        if variable not in heroku_var:
            await zed.edit("**✾╎فـار الاسـم التلقائي غيـر موجـود ❌**\n**✾╎لـ اضـافته بالـرد ع الاسم استخـدم الامـر : ↶**\n `.اضف اسمي التلقائي` \n\n**✾╎قنـاة السـورس : @ZEDThon**")
        else:
            await zed.edit("**✾╎الفـار {} موجـود ☑️**\n**✾╎قيمـة الفـار : ↶**\n `{}` \n\n**✾╎قنـاة السـورس : @ZEDThon**".format(input_str, variable))

    elif input_str == "رسائل الحماية" or input_str == "رسائل الحمايه" or input_str == "رسائل الخاص" or input_str == "رسائل حماية الخاص" or input_str == "عدد التحذيرات":
        variable = gvarstatus("MAX_FLOOD_IN_PMS")
        if variable is None:
            await zed.edit("**✾╎فـار رسائـل الحمايـة غيـر موجـود ❌**\n**✾╎لـ اضـافته بالـرد ع عدد استخـدم الامـر : ↶**\n `.اضف رسائل الحماية` \n\n**✾╎قنـاة السـورس : @ZEDThon**")
        else:
            await zed.edit("**✾╎الفـار {} موجـود ☑️**\n**✾╎قيمـة الفـار : ↶**\n `{}` \n\n**✾╎قنـاة السـورس : @ZEDThon**".format(input_str, variable))

    elif input_str == "صورة الحماية" or input_str == "صوره الحمايه" or input_str == "صورة الحمايه" or input_str == "صوره الحماية":
        variable = gvarstatus("pmpermit_pic")
        if variable is None:
            await zed.edit("**✾╎فـار صـورة الحمايـة غيـر موجـود ❌**\n**✾╎لـ اضـافته بالـرد ع صـورة فقـط استخـدم الامـر : ↶**\n `.اضف صورة الحماية` \n\n**✾╎قنـاة السـورس : @ZEDThon**")
        else:
            await zed.edit("**✾╎الفـار {} موجـود ☑️**\n**✾╎قيمـة الفـار : ↶**\n `{}` \n\n**✾╎قنـاة السـورس : @ZEDThon**".format(input_str, variable))

    elif input_str == "صورة الوقتي" or input_str == "صوره الوقتي":
        variable = gvarstatus("DIGITAL_PIC")
        if variable is None:
            await zed.edit("**✾╎فـار صـورة الوقتـي غيـر موجـود ❌**\n**✾╎لـ اضـافته بالـرد ع صـورة فقـط استخـدم الامـر : ↶**\n `.اضف صورة الوقتي` \n\n**✾╎قنـاة السـورس : @ZEDThon**")
        else:
            await zed.edit("**✾╎الفـار {} موجـود ☑️**\n**✾╎قيمـة الفـار : ↶**\n `{}` \n\n**✾╎قنـاة السـورس : @ZEDThon**".format(input_str, variable))

    elif input_str == "صورة الفحص" or input_str == "صوره الفحص":
        variable = gvarstatus("ALIVE_PIC")
        if variable is None:
            await zed.edit("**✾╎فـار صـورة الفحص غيـر موجـود ❌**\n**✾╎لـ اضـافته بالـرد ع صـورة فقـط استخـدم الامـر : ↶**\n `.اضف صورة الفحص` \n\n**✾╎قنـاة السـورس : @ZEDThon**")
        else:
            await zed.edit("**✾╎الفـار {} موجـود ☑️**\n**✾╎قيمـة الفـار : ↶**\n `{}` \n\n**✾╎قنـاة السـورس : @ZEDThon**".format(input_str, variable))

    elif input_str == "صورة البوت" or input_str == "صوره البوت":
        variable = gvarstatus("BOT_START_PIC")
        if variable is None:
            await zed.edit("**✾╎فـار صـورة ستـارت البـوت غيـر موجـود ❌**\n**✾╎لـ اضـافته بالـرد ع صـورة فقـط استخـدم الامـر : ↶**\n `.اضف صورة البوت` \n\n**✾╎قنـاة السـورس : @ZEDThon**")
        else:
            await zed.edit("**✾╎الفـار {} موجـود ☑️**\n**✾╎قيمـة الفـار : ↶**\n `{}` \n\n**✾╎قنـاة السـورس : @ZEDThon**".format(input_str, variable))

    elif input_str == "صورة الاوامر" or input_str == "صوره الاوامر":
        variable = gvarstatus("CMD_PIC")
        if variable is None:
            await zed.edit("**✾╎فـار صـورة الاوامـر غيـر موجـود ❌**\n**✾╎لـ اضـافته بالـرد ع صـورة فقـط استخـدم الامـر : ↶**\n `.اضف صورة الاوامر` \n\n**✾╎قنـاة السـورس : @ZEDThon**")
        else:
            await zed.edit("**✾╎الفـار {} موجـود ☑️**\n**✾╎قيمـة الفـار : ↶**\n `{}` \n\n**✾╎قنـاة السـورس : @ZEDThon**".format(input_str, variable))

    elif input_str == "صورة السورس" or input_str == "صوره السورس":
        variable = gvarstatus("ALIVE_PIC")
        if variable is None:
            await zed.edit("**✾╎فـار صـورة السـورس غيـر موجـود ❌**\n**✾╎لـ اضـافته بالـرد ع صـورة فقـط استخـدم الامـر : ↶**\n `.اضف صورة السورس` \n\n**✾╎قنـاة السـورس : @ZEDThon**")
        else:
            await zed.edit("**✾╎الفـار {} موجـود ☑️**\n**✾╎قيمـة الفـار : ↶**\n `{}` \n\n**✾╎قنـاة السـورس : @ZEDThon**".format(input_str, variable))

    elif input_str == "صورة الكتم" or input_str == "صوره الكتم":
        variable = gvarstatus("KTM_PIC")
        if variable is None:
            await zed.edit("**✾╎فـار صـورة الكتـم غيـر موجـود ❌**\n**✾╎لـ اضـافته بالـرد ع صـورة فقـط استخـدم الامـر : ↶**\n `.اضف صورة الكتم` \n\n**✾╎قنـاة السـورس : @ZEDThon**")
        else:
            await zed.edit("**✾╎الفـار {} موجـود ☑️**\n**✾╎قيمـة الفـار : ↶**\n `{}` \n\n**✾╎قنـاة السـورس : @ZEDThon**".format(input_str, variable))

    elif input_str == "زخرفة الوقتي" or input_str == "زخرفه الوقتي":
        if Config.HEROKU_API_KEY is None:
            return await ed(event, "✾╎اضبط Var المطلوب في Heroku على وظيفة هذا بشكل طبيعي `HEROKU_API_KEY` اذا كنت لاتعلم اين يوجد فقط اذهب الى حسابك في هيروكو ثم الى الاعدادات ستجده بالاسفل انسخه ودخله في الفار. ")
        if Config.HEROKU_APP_NAME is not None:
            app = Heroku.app(Config.HEROKU_APP_NAME)
        else:
            return await ed(event, "✾╎اضبط Var المطلوب في Heroku على وظيفة هذا بشكل طبيعي `HEROKU_APP_NAME` اسم التطبيق اذا كنت لاتعلم.")
        heroku_var = app.config()
        variable = "ZI_FN"
        if variable not in heroku_var:
            await zed.edit("**✾╎فـار زخرفـة الاسـم الوقتي غيـر موجـود ❌**\n**✾╎لـ اضـافته فقـط استخـدم الامـر : ↶**\n `.الوقتي 1` الـى `.الوقتي 14` \n\n**✾╎قنـاة السـورس : @ZEDThon**")
        else:
            await zed.edit("**✾╎الفـار {} موجـود ☑️**\n**✾╎قيمـة الفـار : ↶**\n `{}` \n\n**✾╎قنـاة السـورس : @ZEDThon**".format(input_str, variable))

    elif input_str == "زخرفة الوقتية" or input_str == "زخرفه الوقتيه" or input_str == "زخرفة الوقتيه" or input_str == "زخرفه الوقتية":
        variable = gvarstatus("DEFAULT_PIC")
        if variable is None:
            await zed.edit("**✾╎فـار زخرفـة الصـورة الوقتيـة غيـر موجـود ❌**\n**✾╎لـ اضـافته فقـط استخـدم الامـر : ↶**\n `.وقتي 1` الـى `.وقتي 17` \n\n**✾╎قنـاة السـورس : @ZEDThon**")
        else:
            await zed.edit("**✾╎الفـار {} موجـود ☑️**\n**✾╎قيمـة الفـار : ↶**\n `{}` \n\n**✾╎قنـاة السـورس : @ZEDThon**".format(input_str, variable))

    elif input_str == "الوقت" or input_str == "الساعه" or input_str == "المنطقه الزمنيه":
        if Config.HEROKU_API_KEY is None:
            return await ed(event, "✾╎اضبط Var المطلوب في Heroku على وظيفة هذا بشكل طبيعي `HEROKU_API_KEY` اذا كنت لاتعلم اين يوجد فقط اذهب الى حسابك في هيروكو ثم الى الاعدادات ستجده بالاسفل انسخه ودخله في الفار. ")
        if Config.HEROKU_APP_NAME is not None:
            app = Heroku.app(Config.HEROKU_APP_NAME)
        else:
            return await ed(event, "✾╎اضبط Var المطلوب في Heroku على وظيفة هذا بشكل طبيعي `HEROKU_APP_NAME` اسم التطبيق اذا كنت لاتعلم.")
        heroku_var = app.config()
        variable = "TZ"
        if variable not in heroku_var:
            await zed.edit("**✾╎فـار المنطقـه الزمنيـه غيـر موجـود ❌**\n**✾╎لـ اضـافته فقـط استخـدم الامـر : ↶**\n `.وقت` واسـم الدولـة \n\n**✾╎قنـاة السـورس : @ZEDThon**")
        else:
            await zed.edit("**✾╎الفـار {} موجـود ☑️**\n**✾╎قيمـة الفـار : ↶**\n `{}` \n\n**✾╎قنـاة السـورس : @ZEDThon**".format(input_str, variable))

    elif input_str == "ايموجي الايدي" or input_str == "ايموجي ايدي" or input_str == "رمز الايدي" or input_str == "رمز ايدي" or input_str == "الرمز ايدي":
        variable = gvarstatus("CUSTOM_ALIVE_EMOJI")
        if variable is None:
            await zed.edit("**✾╎فـار ايموجي/رمز الايدي غيـر موجـود ❌**\n**✾╎لـ اضـافته بالـرد ع الرمـز استخـدم الامـر : ↶**\n `.اضف رمز الايدي` \n\n**✾╎قنـاة السـورس : @ZEDThon**")
        else:
            await zed.edit("**✾╎الفـار {} موجـود ☑️**\n**✾╎قيمـة الفـار : ↶**\n `{}` \n\n**✾╎قنـاة السـورس : @ZEDThon**".format(input_str, variable))
            
    elif input_str == "عنوان الايدي" or input_str == "عنوان ايدي":
        variable = gvarstatus("CUSTOM_ALIVE_TEXT")
        if variable is None:
            await zed.edit("**✾╎فـار نص عنـوان كليشـة الايـدي غيـر موجـود ❌**\n**✾╎لـ اضـافته بالـرد ع الرمـز استخـدم الامـر : ↶**\n `.اضف عنوان الايدي` \n\n**✾╎قنـاة السـورس : @ZEDThon**")
        else:
            await zed.edit("**✾╎الفـار {} موجـود ☑️**\n**✾╎قيمـة الفـار : ↶**\n `{}` \n\n**✾╎قنـاة السـورس : @ZEDThon**".format(input_str, variable))

    elif input_str == "خط الايدي" or input_str == "خط ايدي" or input_str == "خطوط الايدي" or input_str == "خط ايدي":
        variable = gvarstatus("CUSTOM_ALIVE_FONT")
        if variable is None:
            await zed.edit("**✾╎فـار خطـوط كليشـة الايـدي غيـر موجـود ❌**\n**✾╎لـ اضـافته بالـرد ع الرمـز استخـدم الامـر : ↶**\n `.اضف خطوط الايدي` \n\n**✾╎قنـاة السـورس : @ZEDThon**")
        else:
            await zed.edit("**✾╎الفـار {} موجـود ☑️**\n**✾╎قيمـة الفـار : ↶**\n `{}` \n\n**✾╎قنـاة السـورس : @ZEDThon**".format(input_str, variable))

    elif input_str == "لاعب 1":
        variable = gvarstatus("Z_AK")
        if gvarstatus("Z_AK") is None:
            await zed.edit("**✾╎المتغيـر غيـر موجـود ❌**\n\n**✾╎قنـاة السـورس : @ZEDThon**")
        else:
            await zed.edit("**✾╎المتغيـر {} موجـود ☑️**\n**✾╎قيمـة المتغيـر : ↶**\n `{}` \n\n**✾╎قنـاة السـورس : @ZEDThon**".format(input_str, variable))

    elif input_str == "لاعب 2":
        variable = gvarstatus("Z_AK1")
        if gvarstatus("Z_AK1") is None:
            await zed.edit("**✾╎المتغيـر غيـر موجـود ❌**\n\n**✾╎قنـاة السـورس : @ZEDThon**")
        else:
            await zed.edit("**✾╎المتغيـر {} موجـود ☑️**\n**✾╎قيمـة المتغيـر : ↶**\n `{}` \n\n**✾╎قنـاة السـورس : @ZEDThon**".format(input_str, variable))

    elif input_str == "لاعب 3":
        variable = gvarstatus("Z_AK2")
        if gvarstatus("Z_AK2") is None:
            await zed.edit("**✾╎المتغيـر غيـر موجـود ❌**\n\n**✾╎قنـاة السـورس : @ZEDThon**")
        else:
            await zed.edit("**✾╎المتغيـر {} موجـود ☑️**\n**✾╎قيمـة المتغيـر : ↶**\n `{}` \n\n**✾╎قنـاة السـورس : @ZEDThon**".format(input_str, variable))

    elif input_str == "لاعب 4":
        variable = gvarstatus("Z_AK3")
        if gvarstatus("Z_AK3") is None:
            await zed.edit("**✾╎المتغيـر غيـر موجـود ❌**\n\n**✾╎قنـاة السـورس : @ZEDThon**")
        else:
            await zed.edit("**✾╎المتغيـر {} موجـود ☑️**\n**✾╎قيمـة المتغيـر : ↶**\n `{}` \n\n**✾╎قنـاة السـورس : @ZEDThon**".format(input_str, variable))

    elif input_str == "لاعب 5":
        variable = gvarstatus("Z_AK4")
        if gvarstatus("Z_AK4") is None:
            await zed.edit("**✾╎المتغيـر غيـر موجـود ❌**\n\n**✾╎قنـاة السـورس : @ZEDThon**")
        else:
            await zed.edit("**✾╎المتغيـر {} موجـود ☑️**\n**✾╎قيمـة المتغيـر : ↶**\n `{}` \n\n**✾╎قنـاة السـورس : @ZEDThon**".format(input_str, variable))

    elif input_str == "توكن المكافح" or input_str == "كود المكافح" or input_str == "مكافح التخريب" or input_str == "مكافح التفليش":
        if Config.HEROKU_API_KEY is None:
            return await ed(event, "✾╎اضبط Var المطلوب في Heroku على وظيفة هذا بشكل طبيعي `HEROKU_API_KEY` اذا كنت لاتعلم اين يوجد فقط اذهب الى حسابك في هيروكو ثم الى الاعدادات ستجده بالاسفل انسخه ودخله في الفار. ")
        if Config.HEROKU_APP_NAME is not None:
            app = Heroku.app(Config.HEROKU_APP_NAME)
        else:
            return await ed(event, "✾╎اضبط Var المطلوب في Heroku على وظيفة هذا بشكل طبيعي `HEROKU_APP_NAME` اسم التطبيق اذا كنت لاتعلم.")
        heroku_var = app.config()
        variable = "SPAMWATCH_API"
        if variable not in heroku_var:
            await zed.edit("**✾╎فـار توكـن المكـافح غيـر موجـود ❌**\n\n**✾╎قنـاة السـورس : @ZEDThon**")
        else:
            await zed.edit("**✾╎الفـار {} موجـود ☑️**\n**✾╎قيمـة الفـار : ↶**\n `{}` \n\n**✾╎قنـاة السـورس : @ZEDThon**".format(input_str, variable))

    else:
        if input_str:
            return await zed.edit("**✾╎عـذراً .. لايوجـد هنالك فـار بإسـم {} ؟!.. ارسـل (.اوامر الفارات) لـعرض قائمـة الفـارات**".format(input_str))
        return await edit_or_reply(event, "**✾╎عـذراً .. لايوجـد هنالك فـار بإسـم {} ؟!.. ارسـل (.اوامر الفارات) لـعرض قائمـة الفـارات**".format(input_str))


# Copyright (C) 2022 Zed-Thon . All Rights Reserved
@zedub.zed_cmd(pattern="وقت(?:\s|$)([\s\S]*)")
async def variable(event):
    if Config.HEROKU_API_KEY is None:
        return await ed(
            event,
            "✾╎اضبط Var المطلوب في Heroku على وظيفة هذا بشكل طبيعي `HEROKU_API_KEY` اذا كنت لاتعلم اين يوجد فقط اذهب الى حسابك في هيروكو ثم الى الاعدادات ستجده بالاسفل انسخه ودخله في الفار. ",
        )
    if Config.HEROKU_APP_NAME is not None:
        app = Heroku.app(Config.HEROKU_APP_NAME)
    else:
        return await ed(
            event,
            "✾╎اضبط Var المطلوب في Heroku على وظيفة هذا بشكل طبيعي `HEROKU_APP_NAME` اسم التطبيق اذا كنت لاتعلم.",
        )
    input_str = event.text[5:]
    viraq = "Asia/Baghdad"
    vmsr = "Africa/Cairo"
    heroku_var = app.config()
    zed = await edit_or_reply(event, "**✾╎جـاري أعـداد المنطقـه الزمنيـه لـ زدثــون 🌐...**")
    # All Rights Reserved for "Zed-Thon" "زلـزال الهيبـه"
    if input_str == "العراق" or input_str == "عراق":
        variable = "TZ"
        await asyncio.sleep(1.5)
        if variable in heroku_var:
            await zed.edit("**✾╎تم تغييـر المنطقـه الزمنيـه .. بنجـاح ☑️**\n**✾╎المتغير : ↶**\n دولـة `{}` 🇮🇶 \n**✾╎يتم الان اعـادة تشغيـل بـوت زد ثـون يستغـرق الامر 2-1 دقيقـه ▬▭ ...**".format(input_str))
        else:
            await zed.edit("**✾╎تم اضـافـة المنطقـه الزمنيـه .. بنجـاح ☑️**\n**✾╎المضـاف اليـه : ↶**\n دولـة `{}` 🇮🇶 \n**✾╎يتم الان اعـادة تشغيـل بـوت زد ثـون يستغـرق الامر 2-1 دقيقـه ▬▭ ...**".format(input_str))
        heroku_var[variable] = viraq
    elif input_str == "اليمن" or input_str == "يمن":
        variable = "TZ"
        await asyncio.sleep(1.5)
        if variable in heroku_var:
            await zed.edit("**✾╎تم تغييـر المنطقـه الزمنيـه .. بنجـاح ☑️**\n**✾╎المتغير : ↶**\n دولـة `{}` 🇾🇪 \n**✾╎يتم الان اعـادة تشغيـل بـوت زد ثـون يستغـرق الامر 2-1 دقيقـه ▬▭ ...**".format(input_str))
        else:
            await zed.edit("**✾╎تم اضـافـة المنطقـه الزمنيـه .. بنجـاح ☑️**\n**✾╎المضـاف اليـه : ↶**\n دولـة `{}` 🇾🇪 \n**✾╎يتم الان اعـادة تشغيـل بـوت زد ثـون يستغـرق الامر 2-1 دقيقـه ▬▭ ...**".format(input_str))
        heroku_var[variable] = viraq
    elif input_str == "سوريا" or input_str == "سوريه":
        variable = "TZ"
        await asyncio.sleep(1.5)
        if variable in heroku_var:
            await zed.edit("**✾╎تم تغييـر المنطقـه الزمنيـه .. بنجـاح ☑️**\n**✾╎المتغير : ↶**\n دولـة `{}` 🇸🇾 \n**✾╎يتم الان اعـادة تشغيـل بـوت زد ثـون يستغـرق الامر 2-1 دقيقـه ▬▭ ...**".format(input_str))
        else:
            await zed.edit("**✾╎تم اضـافـة المنطقـه الزمنيـه .. بنجـاح ☑️**\n**✾╎المضـاف اليـه : ↶**\n دولـة `{}` 🇸🇾 \n**✾╎يتم الان اعـادة تشغيـل بـوت زد ثـون يستغـرق الامر 2-1 دقيقـه ▬▭ ...**".format(input_str))
        heroku_var[variable] = viraq
    elif input_str == "مصر" or input_str == "المصري" or input_str == "القاهرة":
        variable = "TZ"
        await asyncio.sleep(1.5)
        if variable in heroku_var:
            await zed.edit("**✾╎تم تغييـر المنطقـه الزمنيـه .. بنجـاح ☑️**\n**✾╎المتغير : ↶**\n دولـة `{}` 🇪🇬 \n**✾╎يتم الان اعـادة تشغيـل بـوت زد ثـون يستغـرق الامر 2-1 دقيقـه ▬▭ ...**".format(input_str))
        else:
            await zed.edit("**✾╎تم اضـافـة المنطقـه الزمنيـه .. بنجـاح ☑️**\n**✾╎المضـاف اليـه : ↶**\n دولـة `{}` 🇪🇬 \n**✾╎يتم الان اعـادة تشغيـل بـوت زد ثـون يستغـرق الامر 2-1 دقيقـه ▬▭ ...**".format(input_str))
        heroku_var[variable] = vmsr
 

# Copyright (C) 2022 Zed-Thon . All Rights Reserved
@zedub.zed_cmd(pattern="اضف صورة (الحماية|الحمايه|الفحص|الوقتي|البوت|الاوامر) ?(.*)")
async def _(malatha):
    if malatha.fwd_from:
        return
    zed = await edit_or_reply(malatha, "**✾╎جـاري اضـافة فـار الصـورة الـى بـوتك ...**")
    if not os.path.isdir(Config.TEMP_DIR):
        os.makedirs(Config.TEMP_DIR)
        #     if BOTLOG:
        await malatha.client.send_message(
            BOTLOG_CHATID,
            "**✾╎تم إنشاء حساب Telegraph جديد {} للدورة الحالية‌‌** \n**✾╎لا تعطي عنوان url هذا لأي شخص**".format(
                auth_url
            ),
        )
    optional_title = malatha.pattern_match.group(2)
    if malatha.reply_to_msg_id:
        start = datetime.now()
        r_message = await malatha.get_reply_message()
        input_str = malatha.pattern_match.group(1)
        if input_str in ["الحماية", "الحمايه"]:
            downloaded_file_name = await malatha.client.download_media(
                r_message, Config.TEMP_DIR
            )
            end = datetime.now()
            ms = (end - start).seconds
            await zed.edit(
                f"**✾╎تم تحميل {downloaded_file_name} في وقت {ms} ثانيه.**"
            )
            if downloaded_file_name.endswith((".webp")):
                resize_image(downloaded_file_name)
            try:
                start = datetime.now()
                media_urls = upload_file(downloaded_file_name)
            except exceptions.TelegraphException as exc:
                await zed.edit("**✾╎خطا : **" + str(exc))
                os.remove(downloaded_file_name)
            else:
                end = datetime.now()
                ms_two = (end - start).seconds
                os.remove(downloaded_file_name)
                vinfo = ("https://telegra.ph{}".format(media_urls[0]))
                addgvar("pmpermit_pic", vinfo)
                await zed.edit("**✾╎تم تغييـر صـورة {} .. بنجـاح ☑️**\n**✾╎المتغيـر : ↶**\n `{}` \n\n**✾╎قنـاة السـورس : @ZEDThon**".format(input_str, vinfo))
        elif input_str in ["الفحص", "السورس"]:
            downloaded_file_name = await malatha.client.download_media(
                r_message, Config.TEMP_DIR
            )
            end = datetime.now()
            ms = (end - start).seconds
            await zed.edit(
                f"**✾╎تم تحميل {downloaded_file_name} في وقت {ms} ثانيه.**"
            )
            if downloaded_file_name.endswith((".webp")):
                resize_image(downloaded_file_name)
            try:
                start = datetime.now()
                media_urls = upload_file(downloaded_file_name)
            except exceptions.TelegraphException as exc:
                await zed.edit("**✾╎خطا : **" + str(exc))
                os.remove(downloaded_file_name)
            else:
                end = datetime.now()
                ms_two = (end - start).seconds
                os.remove(downloaded_file_name)
                vinfo = ("https://telegra.ph{}".format(media_urls[0]))
                addgvar("ALIVE_PIC", vinfo)
                await zed.edit("**✾╎تم تغييـر صـورة {} .. بنجـاح ☑️**\n**✾╎المتغيـر : ↶**\n `{}` \n\n**✾╎قنـاة السـورس : @ZEDThon**".format(input_str, vinfo))
        elif input_str in ["البوت", "الستارت"]:
            downloaded_file_name = await malatha.client.download_media(
                r_message, Config.TEMP_DIR
            )
            end = datetime.now()
            ms = (end - start).seconds
            await zed.edit(
                f"**✾╎تم تحميل {downloaded_file_name} في وقت {ms} ثانيه.**"
            )
            if downloaded_file_name.endswith((".webp")):
                resize_image(downloaded_file_name)
            try:
                start = datetime.now()
                media_urls = upload_file(downloaded_file_name)
            except exceptions.TelegraphException as exc:
                await zed.edit("**✾╎خطا : **" + str(exc))
                os.remove(downloaded_file_name)
            else:
                end = datetime.now()
                ms_two = (end - start).seconds
                os.remove(downloaded_file_name)
                vinfo = ("https://telegra.ph{}".format(media_urls[0]))
                addgvar("BOT_START_PIC", vinfo)
                await zed.edit("**✾╎تم تغييـر صـورة {} .. بنجـاح ☑️**\n**✾╎المتغيـر : ↶**\n `{}` \n\n**✾╎قنـاة السـورس : @ZEDThon**".format(input_str, vinfo))
        elif input_str in ["الاوامر", "اللوحه"]:
            downloaded_file_name = await malatha.client.download_media(
                r_message, Config.TEMP_DIR
            )
            end = datetime.now()
            ms = (end - start).seconds
            await zed.edit(
                f"**✾╎تم تحميل {downloaded_file_name} في وقت {ms} ثانيه.**"
            )
            if downloaded_file_name.endswith((".webp")):
                resize_image(downloaded_file_name)
            try:
                start = datetime.now()
                media_urls = upload_file(downloaded_file_name)
            except exceptions.TelegraphException as exc:
                await zed.edit("**✾╎خطا : **" + str(exc))
                os.remove(downloaded_file_name)
            else:
                end = datetime.now()
                ms_two = (end - start).seconds
                os.remove(downloaded_file_name)
                vinfo = ("https://telegra.ph{}".format(media_urls[0]))
                addgvar("CMD_PIC", vinfo)
                await zed.edit("**✾╎تم تغييـر صـورة {} .. بنجـاح ☑️**\n**✾╎المتغيـر : ↶**\n `{}` \n\n**✾╎قنـاة السـورس : @ZEDThon**".format(input_str, vinfo))
        elif input_str in ["السورس", "سورس"]:
            downloaded_file_name = await malatha.client.download_media(
                r_message, Config.TEMP_DIR
            )
            end = datetime.now()
            ms = (end - start).seconds
            await zed.edit(
                f"**✾╎تم تحميل {downloaded_file_name} في وقت {ms} ثانيه.**"
            )
            if downloaded_file_name.endswith((".webp")):
                resize_image(downloaded_file_name)
            try:
                start = datetime.now()
                media_urls = upload_file(downloaded_file_name)
            except exceptions.TelegraphException as exc:
                await zed.edit("**✾╎خطا : **" + str(exc))
                os.remove(downloaded_file_name)
            else:
                end = datetime.now()
                ms_two = (end - start).seconds
                os.remove(downloaded_file_name)
                vinfo = ("https://telegra.ph{}".format(media_urls[0]))
                addgvar("ALIVE_PIC", vinfo)
                await zed.edit("**✾╎تم تغييـر صـورة {} .. بنجـاح ☑️**\n**✾╎المتغيـر : ↶**\n `{}` \n\n**✾╎قنـاة السـورس : @ZEDThon**".format(input_str, vinfo))
        elif input_str in ["الكتم", "كتم"]:
            downloaded_file_name = await malatha.client.download_media(
                r_message, Config.TEMP_DIR
            )
            end = datetime.now()
            ms = (end - start).seconds
            await zed.edit(
                f"**✾╎تم تحميل {downloaded_file_name} في وقت {ms} ثانيه.**"
            )
            if downloaded_file_name.endswith((".webp")):
                resize_image(downloaded_file_name)
            try:
                start = datetime.now()
                media_urls = upload_file(downloaded_file_name)
            except exceptions.TelegraphException as exc:
                await zed.edit("**✾╎خطا : **" + str(exc))
                os.remove(downloaded_file_name)
            else:
                end = datetime.now()
                ms_two = (end - start).seconds
                os.remove(downloaded_file_name)
                vinfo = ("https://telegra.ph{}".format(media_urls[0]))
                addgvar("KTM_PIC", vinfo)
                await zed.edit("**✾╎تم تغييـر صـورة {} .. بنجـاح ☑️**\n**✾╎المتغيـر : ↶**\n `{}` \n\n**✾╎قنـاة السـورس : @ZEDThon**".format(input_str, vinfo))
        elif input_str in ["الوقتي", "البروفايل"]:
            downloaded_file_name = await malatha.client.download_media(
                r_message, Config.TEMP_DIR
            )
            end = datetime.now()
            ms = (end - start).seconds
            await zed.edit(
                f"**✾╎تم تحميل {downloaded_file_name} في وقت {ms} ثانيه.**"
            )
            if downloaded_file_name.endswith((".webp")):
                resize_image(downloaded_file_name)
            try:
                start = datetime.now()
                media_urls = upload_file(downloaded_file_name)
            except exceptions.TelegraphException as exc:
                await zed.edit("**✾╎خطا : **" + str(exc))
                os.remove(downloaded_file_name)
            else:
                end = datetime.now()
                ms_two = (end - start).seconds
                os.remove(downloaded_file_name)
                vinfo = ("https://telegra.ph{}".format(media_urls[0]))
                addgvar("DIGITAL_PIC", vinfo)
                await zed.edit("**✾╎تم تغييـر صـورة {} .. بنجـاح ☑️**\n**✾╎المتغيـر : ↶**\n `{}` \n\n**✾╎قنـاة السـورس : @ZEDThon**".format(input_str, vinfo))


    else:
        await zed.edit(
            "**✾╎بالـرد ع صـورة لتعييـن الفـار ...**",
        )


def resize_image(image):
    im = Image.open(image)
    im.save(image, "PNG")



# Copyright (C) 2022 vtvit . All Rights Reserved
@iqub.iq_cmd(pattern="فەرمانی ڤارەکان")
async def cmd(iquser):
    await edit_or_reply(iquser, iquserVP_cmd)

