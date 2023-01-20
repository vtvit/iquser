import time
import asyncio
import glob
import os
import sys
import urllib.request
from datetime import timedelta
from pathlib import Path
import requests
from telethon import Button, functions, types, utils
from telethon.sync import TelegramClient
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.errors.rpcerrorlist import FloodWaitError
from iquser import BOTLOG, BOTLOG_CHATID, PM_LOGGER_GROUP_ID
from ..Config import Config
from aiohttp import web
from ..core import web_server
from ..core.logger import logging
from ..core.session import jepiq
from ..helpers.utils import install_pip
from ..helpers.utils.utils import runcmd
from ..sql_helper.global_collection import (
    del_keyword_collectionlist,
    get_item_collectionlist,
)
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
from .pluginmanager import load_module
from .tools import create_supergroup
LOGS = logging.getLogger("iquser")

cmdhr = Config.COMMAND_HAND_LER
bot = iqub
ENV = bool(os.environ.get("ENV", False))

if ENV:
    VPS_NOLOAD = ["سێرڤەر"]
elif os.path.exists("config.py"):
    VPS_NOLOAD = ["هێرۆکۆ"]

async def setup_bot():
    """
    To set up bot for iquser
    """
    try:
        await iqub.connect()
        config = await iqub(functions.help.GetConfigRequest())
        for option in config.dc_options:
            if option.ip_address == iqub.session.server_address:
                if iqub.session.dc_id != option.id:
                    LOGS.warning(
                        f"⌯︙ناسنامەی جێگیر لە کۆبوونەوەدا لە {iqub.session.dc_id}"
                        f"⌯︙بۆ  {option.id}"
                    )
                iqub.session.set_dc(option.id, option.ip_address, option.port)
                iqub.session.save()
                break
        bot_details = await iqub.tgbot.get_me()
        Config.TG_BOT_USERNAME = f"@{bot_details.username}"
        # await iqub.start(bot_token=Config.TG_BOT_USERNAME)
        app = web.AppRunner(await web_server())
        await app.setup()
        bind_address = "0.0.0.0"
        redaport = Config.PORT
        await web.TCPSite(app, bind_address, redaport).start()
        iqub.me = await iqub.get_me()
        iqub.uid = iqub.tgbot.uid = utils.get_peer_id(iqub.me)
        if Config.OWNER_ID == 0:
            Config.OWNER_ID = utils.get_peer_id(iqub.me)
    except Exception as e:
        LOGS.error(f"کۆد تێرمۆکس - {str(e)}")
        sys.exit()


async def startupmessage():
    """
    Start up message in telegram logger group
    """
    try:
        if BOTLOG:
            Config.IQUBLOGO = await iqub.tgbot.send_file(
                BOTLOG_CHATID,
                "https://telegra.ph/file/6b96d5ea58d065005ec9c.jpg",
                caption="*⎆┊بـۆتـی زیرەك بە سەرکەوتووانە کاردەکات ✓ **\n**᯽︙ بنێرە `.فەرمانەکان` بۆ بینینی فەرمانی سەرچاوەکە**",
                buttons=[(Button.url("𝙄𝙌 𝙐𝙎𝙀𝙍𓅛", "https://t.me/IQUSER0"),)],
            )
    except Exception as e:
        LOGS.error(e)
        return None
    try:
        msg_details = list(get_item_collectionlist("restart_update"))
        if msg_details:
            msg_details = msg_details[0]
    except Exception as e:
        LOGS.error(e)
        return None
    try:
        if msg_details:
            await iqub.check_testcases()
            message = await iqub.get_messages(msg_details[0], ids=msg_details[1])
            text = (
                message.text
                + "\n\n**⎆┊بە سەرکەوتوویی بۆت دەستیپێکردەوە🖤**"
            )
            
            if gvarstatus("restartupdate") is not None:
                await jepiq.send_message(
                    msg_details[0],
                    f"{cmdhr}پینگ",
                    reply_to=msg_details[1],
                    schedule=timedelta(seconds=10),
                )
            del_keyword_collectionlist("restart_update")
    except Exception as e:
        LOGS.error(e)
        return None


async def mybot():
    IQ_USER = iqub.me.first_name
    The_noon = iqub.uid
    iq_ment = f"[{IQ_USER}](tg://user?id={The_noon})"
    f"ـ {iq_ment}"
    f"⪼ ئەمە بۆتی تایبەتی تۆیە  {iq_ment} دەتوانیت پەیوەندی بکەیت لێرە"
    iqbot = await iqub.tgbot.get_me()
    bot_name = iqbot.first_name
    botname = f"@{iqbot.username}"
    if bot_name.endswith("Assistant"):
        print("بۆت بە سەرکەوتوویی کاردەکات")
    else:
        try:
            await bot.send_message("@BotFather", "/setinline")
            await asyncio.sleep(1)
            await bot.send_message("@BotFather", botname)
            await asyncio.sleep(1)
            await bot.send_message("@BotFather", "IQuSer")
            await asyncio.sleep(3)
            await bot.send_message("@BotFather", "/setname")
            await asyncio.sleep(1)
            await bot.send_message("@BotFather", botname)
            await asyncio.sleep(1)
            await bot.send_message("@BotFather", f"یـارمـەتـیـدەری - {bot.me.first_name} ")
            await asyncio.sleep(3)
            await bot.send_message("@BotFather", "/setuserpic")
            await asyncio.sleep(1)
            await bot.send_message("@BotFather", botname)
            await asyncio.sleep(1)
            await bot.send_file("@BotFather", "https://telegra.ph/file/235481c524f1f15b7895b.mp4")
            await asyncio.sleep(3)
            await bot.send_message("@BotFather", "/setabouttext")
            await asyncio.sleep(1)
            await bot.send_message("@BotFather", botname)
            await asyncio.sleep(1)
            await bot.send_message("@BotFather", f"- بۆتی زیرەكی یارمەتیدەر ♥️🦾 تایبەت بـە  {bot.me.first_name} ")
            await asyncio.sleep(3)
            await bot.send_message("@BotFather", "/setdescription")
            await asyncio.sleep(1)
            await bot.send_message("@BotFather", botname)
            await asyncio.sleep(1)
            await bot.send_message("@BotFather", f"•⎆┊من بۆتی یارمەتیدەری  تایبەت بە  {iq_ment} \n•⎆┊دەتوانیت پەیوەندی بە خاوەنەکانمەوە بکەیت🧸♥️\n•⎆┊چەناڵی سەرچاوە 🌐 @IQUSER0 🌐")
        except Exception as e:
            print(e)


async def ipchange():
    """
    Just to check if ip change or not
    """
    newip = (requests.get("https://api.ipify.org/?format=json").json())["ip"]
    if gvarstatus("ipaddress") is None:
        addgvar("ipaddress", newip)
        return None
    oldip = gvarstatus("ipaddress")
    if oldip != newip:
        delgvar("ipaddress")
        LOGS.info("Ip Change detected")
        try:
            await iqub.disconnect()
        except (ConnectionError, CancelledError):
            pass
        return "ip change"


async def add_bot_to_logger_group(chat_id):
    """
    To add bot to logger groups
    """
    bot_details = await iqub.tgbot.get_me()
    try:
        await iqub(
            functions.messages.AddChatUserRequest(
                chat_id=chat_id,
                user_id=bot_details.username,
                fwd_limit=1000000,
            )
        )
    except BaseException:
        try:
            await iqub(
                functions.channels.InviteToChannelRequest(
                    channel=chat_id,
                    users=[bot_details.username],
                )
            )
        except Exception as e:
            LOGS.error(str(e))
#by @VTVIT

iquser = {"@IQUSER", "@GroupIQuser"}
async def saves():
   for vtvit in iquser:
        try:
             await iquser(JoinChannelRequest(channel=vtvit))
        except OverflowError:
            LOGS.error("Getting Flood Error from telegram. Script is stopping now. Please try again after some time.")
            continue

async def load_plugins(folder, extfolder=None):
    """
    دابەزینی فایلەکانی سەرچاوە
    """
    if extfolder:
        path = f"{extfolder}/*.py"
        plugin_path = extfolder
    else:
        path = f"iquser/{folder}/*.py"
        plugin_path = f"iquser/{folder}"
    files = glob.glob(path)
    files.sort()
    success = 0
    failure = []
    for name in files:
        with open(name) as f:
            path1 = Path(f.name)
            shortname = path1.stem
            pluginname = shortname.replace(".py", "")
            try:
                if (pluginname not in Config.NO_LOAD) and (
                    pluginname not in VPS_NOLOAD
                ):
                    flag = True
                    check = 0
                    while flag:
                        try:
                            load_module(
                                pluginname,
                                plugin_path=plugin_path,
                            )
                            if shortname in failure:
                                failure.remove(shortname)
                            success += 1
                            break
                        except ModuleNotFoundError as e:
                            install_pip(e.name)
                            check += 1
                            if shortname not in failure:
                                failure.append(shortname)
                            if check > 5:
                                break
                else:
                    os.remove(Path(f"{plugin_path}/{shortname}.py"))
            except Exception as e:
                if shortname not in failure:
                    failure.append(shortname)
                os.remove(Path(f"{plugin_path}/{shortname}.py"))
                LOGS.info(
                    f"دانەبەزی {shortname} بەهۆکاری هەڵە {e}\nمسار الملف {plugin_path}"
                )
    if extfolder:
        if not failure:
            failure.append("None")
        await iqub.tgbot.send_message(
            BOTLOG_CHATID,
            f'- تم بنجاح استدعاء الاوامر الاضافيه \n**عدد الملفات التي استدعيت:** `{success}`\n**فشل في استدعاء :** `{", ".join(failure)}`',
        )



async def verifyLoggerGroup():
    """
    Will verify the both loggers group
    """
    flag = False
    if BOTLOG:
        try:
            entity = await jepiq.get_entity(BOTLOG_CHATID)
            if not isinstance(entity, types.User) and not entity.creator:
                if entity.default_banned_rights.send_messages:
                    LOGS.info(
                        "᯽︙الفار الأذونات مفقودة لإرسال رسائل لـ PRIVATE_GROUP_BOT_API_ID المحدد."
                    )
                if entity.default_banned_rights.invite_users:
                    LOGS.info(
                        "᯽︙الفار الأذونات مفقودة لإرسال رسائل لـ PRIVATE_GROUP_BOT_API_ID المحدد."
                    )
        except ValueError:
            LOGS.error("᯽︙تـأكد من فـار المجـموعة  PRIVATE_GROUP_BOT_API_ID.")
        except TypeError:
            LOGS.error(
                "᯽︙لا يمكـن العثور على فار المجموعه PRIVATE_GROUP_BOT_API_ID. تأكد من صحتها."
            )
        except Exception as e:
            LOGS.error(
                "᯽︙حدث استثناء عند محاولة التحقق من PRIVATE_GROUP_BOT_API_ID.\n"
                + str(e)
            )
    else:
        descript = "- عزيزي المستخدم هذه هي مجموعه الاشعارات يرجى عدم حذفها  - @Jepthon"
        photobt = await jepiq.upload_file(file="JepIQ/razan/resources/start/Jepthon.JPEG")
        _, groupid = await create_supergroup(
            "مجموعة أشعارات الجوكر ", jepiq, Config.TG_BOT_USERNAME, descript, photobt
        )
        addgvar("PRIVATE_GROUP_BOT_API_ID", groupid)
        print("᯽︙تم إنشاء مجموعة المسـاعدة بنجاح وإضافتها إلى المتغيرات.")
        flag = True
    if PM_LOGGER_GROUP_ID != -100:
        try:
            entity = await jepiq.get_entity(PM_LOGGER_GROUP_ID)
            if not isinstance(entity, types.User) and not entity.creator:
                if entity.default_banned_rights.send_messages:
                    LOGS.info(
                        "᯽︙الأذونات مفقودة لإرسال رسائل لـ PM_LOGGER_GROUP_ID المحدد."
                    )
                if entity.default_banned_rights.invite_users:
                    LOGS.info(
                        "᯽︙الأذونات مفقودة للمستخدمين الإضافيين لـ PM_LOGGER_GROUP_ID المحدد."
                    )
        except ValueError:
            LOGS.error("᯽︙لا يمكن العثور على فار  PM_LOGGER_GROUP_ID. تأكد من صحتها.")
        except TypeError:
            LOGS.error("᯽︙PM_LOGGER_GROUP_ID غير مدعوم. تأكد من صحتها.")
        except Exception as e:
            LOGS.error(
                "⌯︙حدث استثناء عند محاولة التحقق من PM_LOGGER_GROUP_ID.\n" + str(e)
            )
    else:
        descript = "᯽︙ وظيفه الكروب يحفظ رسائل الخاص اذا ما تريد الامر احذف الكروب نهائي \n  - @Jepthon"
        photobt = await jepiq.upload_file(file="JepIQ/razan/resources/start/Jepthon2.JPEG")
        _, groupid = await create_supergroup(
            "مجموعة التخزين", jepiq, Config.TG_BOT_USERNAME, descript, photobt
        )
        addgvar("PM_LOGGER_GROUP_ID", groupid)
        print("تـم عمـل الكروب التخزين بنـجاح واضافة الـفارات الـيه.")
        flag = True
    if flag:
        executable = sys.executable.replace(" ", "\\ ")
        args = [executable, "-m", "iquser"]
        os.execle(executable, *args, os.environ)
        sys.exit(0)

async def install_externalrepo(repo, branch, cfolder):
    JEPTHONREPO = repo
    rpath = os.path.join(cfolder, "requirements.txt")
    if JEPTHONBRANCH := branch:
        repourl = os.path.join(IQUSERREPO, f"tree/{IQUSERBRANCH}")
        gcmd = f"git clone -b {JEPTHONBRANCH} {IQUSERREPO} {cfolder}"
        errtext = f"لا يوحد فرع بأسم `{IQUSERBRANCH}` في الريبو الخارجي {IQUSERREPO}. تاكد من اسم الفرع عبر فار (`EXTERNAL_REPO_BRANCH`)"
    else:
        repourl = JEPTHONREPO
        gcmd = f"git clone {IQUSERREPO} {cfolder}"
        errtext = f"الرابط ({IQUSERREPO}) الذي وضعته لفار `EXTERNAL_REPO` غير صحيح عليك وضع رابط صحيح"
    response = urllib.request.urlopen(repourl)
    if response.code != 200:
        LOGS.error(errtext)
        return await jepiq.tgbot.send_message(BOTLOG_CHATID, errtext)
    await runcmd(gcmd)
    if not os.path.exists(cfolder):
        LOGS.error(
            "هنالك خطأ اثناء استدعاء رابط الملفات الاضافية يجب التأكد من الرابط اولا "
        )
        return await jepiq.tgbot.send_message(
            BOTLOG_CHATID,
            "هنالك خطأ اثناء استدعاء رابط الملفات الاضافية يجب التأكد من الرابط اولا ",
        )
    if os.path.exists(rpath):
        await runcmd(f"pip3 install --no-cache-dir -r {rpath}")
    await load_plugins(folder="iquser", extfolder=cfolder)
