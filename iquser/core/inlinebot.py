import json
import math
import os
import random
import re
import time
from uuid import uuid4

from telethon import Button, types
from telethon.errors import QueryIdInvalidError
from telethon.events import CallbackQuery, InlineQuery
from youtubesearchpython import VideosSearch

from iquser import iqub

from ..assistant.inlinefm import get_manager
from ..Config import Config
from ..helpers.functions import rand_key
from ..helpers.functions.utube import (
    download_button,
    get_yt_video_id,
    get_ytthumb,
    result_formatter,
    ytsearch_data,
)
from ..plugins import mention
from ..sql_helper.globals import gvarstatus
from . import CMD_INFO, GRP_INFO, PLG_INFO, check_owner
from .logger import logging

LOGS = logging.getLogger(__name__)

BTN_URL_REGEX = re.compile(r"(\[([^\[]+?)\]\<buttonurl:(?:/{0,2})(.+?)(:same)?\>)")
ROZLOGO = "https://telegra.ph/file/5b7361f0bec46b646b877.mp4"
tr = Config.COMMAND_HAND_LER

def getkey(val):
    for key, value in GRP_INFO.items():
        for plugin in value:
            if val == plugin:
                return key
    return None


def ibuild_keyboard(buttons):
    keyb = []
    for btn in buttons:
        if btn[2] and keyb:
            keyb[-1].append(Button.url(btn[0], btn[1]))
        else:
            keyb.append([Button.url(btn[0], btn[1])])
    return keyb


def main_menu():
    text = f"**🧑🏻‍💻┊بەخێربێی ئەزیزم {mention}**\n**🛂┊بۆ لیستی فەرمانەکانی یارمەتیدەر \n**⋆─┄─┄─┄─ ɪǫᴜsᴇʀ ─┄─┄─┄─⋆**\n[ᯓ 𝙄𝙌𝙐𝙎𝙀𝙍 メ 🦾♥️](https://t.me/IQUSER0)\n\n"
    if Config.iqub:
        buttons = [
            (Button.inline("ℹ️ زانیاری فایلەکان", data="check"),),
            (
                Button.inline(
                    f"فەرمانی بەڕێوبەر 👮‍ ", data="admin_menu"
                ),
                Button.inline(f"فەرمانی بۆت 🤖", data="bot_menu"),
            ),
            (
                Button.inline(f"فەرمانی ڕابواردن 🎮", data="fun_menu"),
                Button.inline(f"فەرمانی خزمەتگوزاریەکان 🧩", data="misc_menu"),
            ),
            (
                Button.inline(f"ئامێرەکان 💡", data="tools_menu"),
                Button.inline(f"هاوپێچەکان 🖥", data="utils_menu"),
            ),
            (
                Button.inline(f"گەڕان و داگرتن 🪄", data="extra_menu"),
                Button.inline(
                    f"ئەوانی تر 🖨", data="useless_menu"
                ),
            ),
            (Button.inline("🔒 داخستن", data="close"),),
        ]
    else:
        buttons = [
            (Button.inline("ℹ️ زانیاری فایلەکان", data="check"),),
            (
                Button.inline(
                    f"فەرمانی بەڕێوبەر 👮‍ ", data="admin_menu"
                ),
                Button.inline(f"فەرمانی بۆت  🤖", data="bot_menu"),
            ),
            (
                Button.inline(f"فەرمانی ڕابواردن 🎮", data="fun_menu"),
                Button.inline(f"فەرمانی خزمەتگوزاریەکان 🧩", data="misc_menu"),
            ),
            (
                Button.inline(f"ئامێرەکان 💡", data="tools_menu"),
                Button.inline(f"هاوپێچەکان 🖥", data="utils_menu"),
            ),
            (
                Button.inline(f"گەڕان و داگرتن 🪄", data="extra_menu"),
                Button.inline("🔒 داخستن ", data="close"),
            ),
        ]

    return text, buttons


def command_in_category(cname):
    cmds = 0
    for i in GRP_INFO[cname]:
        for _ in PLG_INFO[i]:
            cmds += 1
    return cmds


def paginate_help(
    page_number,
    loaded_plugins,
    prefix,
    plugins=True,
    category_plugins=None,
    category_pgno=0,
):  # sourcery no-metrics
    try:
        number_of_rows = int(gvarstatus("NO_OF_ROWS_IN_HELP") or 5)
    except (ValueError, TypeError):
        number_of_rows = 5
    try:
        number_of_cols = int(gvarstatus("NO_OF_COLUMNS_IN_HELP") or 2)
    except (ValueError, TypeError):
        number_of_cols = 2
    HELP_EMOJI = gvarstatus("HELP_EMOJI") or " "
    helpable_plugins = [p for p in loaded_plugins if not p.startswith("_")]
    helpable_plugins = sorted(helpable_plugins)
    if len(HELP_EMOJI) == 2:
        if plugins:
            modules = [
                Button.inline(
                    f"{HELP_EMOJI[0]} {x} {HELP_EMOJI[1]}",
                    data=f"{x}_prev(1)_command_{prefix}_{page_number}",
                )
                for x in helpable_plugins
            ]
        else:
            modules = [
                Button.inline(
                    f"{HELP_EMOJI[0]} {x} {HELP_EMOJI[1]}",
                    data=f"{x}_cmdhelp_{prefix}_{page_number}_{category_plugins}_{category_pgno}",
                )
                for x in helpable_plugins
            ]
    elif plugins:
        modules = [
            Button.inline(
                f"{HELP_EMOJI} {x} {HELP_EMOJI}",
                data=f"{x}_prev(1)_command_{prefix}_{page_number}",
            )
            for x in helpable_plugins
        ]
    else:
        modules = [
            Button.inline(
                f"{HELP_EMOJI} {x} {HELP_EMOJI}",
                data=f"{x}_cmdhelp_{prefix}_{page_number}_{category_plugins}_{category_pgno}",
            )
            for x in helpable_plugins
        ]
    if number_of_cols == 1:
        pairs = list(zip(modules[::number_of_cols]))
    elif number_of_cols == 2:
        pairs = list(zip(modules[::number_of_cols], modules[1::number_of_cols]))
    else:
        pairs = list(
            zip(
                modules[::number_of_cols],
                modules[1::number_of_cols],
                modules[2::number_of_cols],
            )
        )
    if len(modules) % number_of_cols == 1:
        pairs.append((modules[-1],))
    elif len(modules) % number_of_cols == 2:
        pairs.append((modules[-2], modules[-1]))
    max_num_pages = math.ceil(len(pairs) / number_of_rows)
    modulo_page = page_number % max_num_pages
    if plugins:
        if len(pairs) > number_of_rows:

            pairs = pairs[
                modulo_page * number_of_rows : number_of_rows * (modulo_page + 1)
            ] + [
                (
                    Button.inline("⌫", data=f"{prefix}_prev({modulo_page})_plugin"),
                    Button.inline("⚙️ سەرەکی", data="mainmenu"),
                    Button.inline("⌦", data=f"{prefix}_next({modulo_page})_plugin"),
                )
            ]
        else:
            pairs = pairs + [(Button.inline("⚙️ سەرەکی", data="mainmenu"),)]
    elif len(pairs) > number_of_rows:
        if category_pgno < 0:
            category_pgno = len(pairs) + category_pgno
        pairs = pairs[
            modulo_page * number_of_rows : number_of_rows * (modulo_page + 1)
        ] + [
            (
                Button.inline(
                    "⌫",
                    data=f"{prefix}_prev({modulo_page})_command_{category_plugins}_{category_pgno}",
                ),
                Button.inline(
                    "⬅️ گەڕانەوە ",
                    data=f"back_plugin_{category_plugins}_{category_pgno}",
                ),
                Button.inline(
                    "⌦",
                    data=f"{prefix}_next({modulo_page})_command_{category_plugins}_{category_pgno}",
                ),
            )
        ]
    else:
        if category_pgno < 0:
            category_pgno = len(pairs) + category_pgno
        pairs = pairs + [
            (
                Button.inline(
                    "⬅️ گەڕانەوە ",
                    data=f"back_plugin_{category_plugins}_{category_pgno}",
                ),
            )
        ]
    return pairs


@iqub.tgbot.on(InlineQuery)
async def inline_handler(event):  # sourcery no-metrics
    builder = event.builder
    result = None
    query = event.text
    string = query.lower()
    query.split(" ", 2)
    str_y = query.split(" ", 1)
    string.split()
    query_user_id = event.query.user_id
    if query_user_id == Config.OWNER_ID or query_user_id in Config.SUDO_USERS:
        hmm = re.compile("troll (.*) (.*)")
        match = re.findall(هم, query)
        inf = re.compile("نهێنی (.*) (.*)")
        match2 = re.findall(inf, query)
        hid = re.compile("شاردنەوە (.*)")
        match3 = re.findall(hid, query)
        if query.startswith("*iqub*"):
            buttons = [
                (
                    Button.inline("Stats", data="stats"),
                    Button.url("𝗜𝗤𝗨𝗦𝗘𝗥 𓅛", "https://t.me/IQUSER0"),
                )
            ]
            ALIVE_PIC = gvarstatus("ALIVE_PIC")
            IALIVE_PIC = gvarstatus("IALIVE_PIC")
            if IALIVE_PIC:
                ROZE = [x for x in IALIVE_PIC.split()]
                PIC = list(ROZE)
                I_IMG = random.choice(PIC)
            if not IALIVE_PIC and ALIVE_PIC:
                ROZE = [x for x in ALIVE_PIC.split()]
                PIC = list(ROZE)
                ROZE_IMG = random.choice(PIC)
            elif not IALIVE_PIC:
                ROZE_IMG = None
            if ROZE_IMG and I_IMG.endswith((".jpg", ".png")):
                result = builder.photo(
                    ROZE_IMG,
                    text=query,
                    buttons=buttons,
                )
            elif I_IMG:
                result = builder.document(
                    I_IMG,
                    title="Alive BOT",
                    text=query,
                    buttons=buttons,
                )
            else:
                result = builder.article(
                    title="Alive BOT",
                    text=query,
                    buttons=buttons,
                )
            await event.answer([result] if result else None)
        elif query.startswith("Inline buttons"):
            markdown_note = query[14:]
            prev = 0
            note_data = ""
            buttons = []
            for match in BTN_URL_REGEX.finditer(markdown_note):
                n_escapes = 0
                to_check = match.start(1) - 1
                while to_check > 0 and markdown_note[to_check] == "\\":
                    n_escapes += 1
                    to_check -= 1
                if n_escapes % 2 == 0:
                    buttons.append(
                        (match.group(2), match.group(3), bool(match.group(4)))
                    )
                    note_data += markdown_note[prev : match.start(1)]
                    prev = match.end(1)
                elif n_escapes % 2 == 1:
                    note_data += markdown_note[prev:to_check]
                    prev = match.start(1) - 1
                else:
                    break
            else:
                note_data += markdown_note[prev:]
            message_text = note_data.strip()
            tl_ib_buttons = ibuild_keyboard(buttons)
            result = builder.article(
                title="Inline creator",
                text=message_text,
                buttons=tl_ib_buttons,
                link_preview=False,
            )
            await event.answer([result] if result else None)
        elif match:
            query = query[7:]
            user, txct = query.split(" ", 1)
            builder = event.builder
            troll = os.path.join("./iquser", "troll.txt")
            try:
                jsondata = json.load(open(troll))
            except Exception:
                jsondata = False
            try:
                # if u is user id
                u = int(user)
                try:
                    u = await event.client.get_entity(u)
                    if u.username:
                        razan = f"[{u.first_name}](tg://user?id={u.id})"
                    else:
                        razan = f"@{u.username}"
                    u = int(u.id)
                except ValueError:
                    # ValueError: Could not find the input entity
                    razan = f"[user](tg://user?id={u})"
            except ValueError:
                # if u is username
                try:
                    u = await event.client.get_entity(user)
                except ValueError:
                    return
                if u.username:
                    razan = f"[{u.first_name}](tg://user?id={u.id})"
                else:
                    razan = f"@{u.username}"
                u = int(u.id)
            except Exception:
                return
            timestamp = int(time.time() * 2)
            newtroll = {str(timestamp): {"userid": u, "text": txct}}

            buttons = [Button.inline("کࢪدنِٰــۛــەوٰەی نِٰــۛــآمِٰــۛــە 𖡟 🧾", data=f"troll_{timestamp}")]
            result = builder.article(
                title="نــٖ‌ـ‌ــآمــٖ‌ـ‌ـەی نــٖ‌ـ‌ــهہـێنــٖ‌ـ‌ــی",
                text=f"ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗜𝗤𝗨𝗦𝗘𝗥  **-نــٖ‌ـ‌ــآمــٖ‌ـ‌ــەی نــٖ‌ـ‌ــهہـێنــٖ‌ـ‌ــی 🗳**\n⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆\n\n**⌔╎نامەکە بۆ** {razan} \n**⌔╎تەڻھا ئەو دەتوانێت بیکاتەوە**",
                buttons=buttons,
            )
            await event.answer([result] if result else None)
            if jsondata:
                jsondata.update(newtroll)
                json.dump(jsondata, open(troll, "w"))
            else:
                json.dump(newtroll, open(troll, "w"))
        elif match2:
            query = query[7:]
            user, txct = query.split(" ", 1)
            builder = event.builder
            secret = os.path.join("./iquser", "secrets.txt")
            try:
                jsondata = json.load(open(secret))
            except Exception:
                jsondata = False
            try:
                # if u is user id
                u = int(user)
                try:
                    u = await event.client.get_entity(u)
                    if u.first_name:
                        razan = f"[{u.first_name}](tg://user?id={u.id})"
                    else:
                        razan = f"@{u.username}"
                    u = int(u.id)
                except ValueError:
                    # ValueError: Could not find the input entity
                    razan = f"[user](tg://user?id={u})"
            except ValueError:
                # if u is username
                try:
                    u = await event.client.get_entity(user)
                except ValueError:
                    return
                if u.first_name:
                    razan = f"[{u.first_name}](tg://user?id={u.id})"
                else:
                    razan = f"@{u.username}"
                u = int(u.id)
            except Exception:
                return
            timestamp = int(time.time() * 2)
            newsecret = {str(timestamp): {"userid": u, "text": txct}}

            buttons = [Button.inline("کردنەوەی نامەی نهێنی 🗳", data=f"secret_{timestamp}")]
            result = builder.article(
                title="** نامەی نهێنی **",
                text=f"ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗜𝗤𝗨𝗦𝗘𝗥 **- نامەی نهێنی 📠**\n⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆\n\n**⌔╎نامەکە بۆ** {razan} \n**⌔╎تەنھا ئەو دەتوانێت بیکاتەوە**",
                buttons=buttons,
            )
            await event.answer([result] if result else None)
            if jsondata:
                jsondata.update(newsecret)
                json.dump(jsondata, open(secret, "w"))
            else:
                json.dump(newsecret, open(secret, "w"))
        elif match3:
            query = query[5:]
            builder = event.builder
            hide = os.path.join("./iquser", "hide.txt")
            try:
                jsondata = json.load(open(hide))
            except Exception:
                jsondata = False
            timestamp = int(time.time() * 2)
            newhide = {str(timestamp): {"text": query}}

            buttons = [Button.inline("پیشاندانی نامەکە 📃", data=f"hide_{timestamp}")]
            result = builder.article(
                title="**⌔╎نامەی شاراوە 📟**",
                text=f"ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗜𝗤𝗨𝗦𝗘𝗥   **- نامەی شاراوە 📟**\n⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆\n\n**⌔╎دەست بنێ بێرە بۆ پیشاندانی نامەکە**",
                buttons=buttons,
            )
            await event.answer([result] if result else None)
            if jsondata:
                jsondata.update(newhide)
                json.dump(jsondata, open(hide, "w"))
            else:
                json.dump(newhide, open(hide, "w"))
        elif string == "help":
            _result = main_menu()
            result = builder.article(
                title="© iquser Help",
                description="Help menu for iquser",
                text=_result[0],
                buttons=_result[1],
                link_preview=False,
            )
            await event.answer([result] if result else None)
        elif str_y[0].lower() == "ytdl" and len(str_y) == 2:
            link = get_yt_video_id(str_y[1].strip())
            found_ = True
            if link is None:
                search = VideosSearch(str_y[1].strip(), limit=15)
                resp = (search.result()).get("result")
                if len(resp) == 0:
                    found_ = False
                else:
                    outdata = await result_formatter(resp)
                    key_ = rand_key()
                    ytsearch_data.store_(key_, outdata)
                    buttons = [
                        Button.inline(
                            f"1 / {len(outdata)}",
                            data=f"ytdl_next_{key_}_1",
                        ),
                        Button.inline(
                            "لیستەکان 📜",
                            data=f"ytdl_listall_{key_}_1",
                        ),
                        Button.inline(
                            "⬇️  داگرتن",
                            data=f'ytdl_download_{outdata[1]["video_id"]}_0',
                        ),
                    ]
                    caption = outdata[1]["message"]
                    photo = await get_ytthumb(outdata[1]["video_id"])
            else:
                caption, buttons = await download_button(link, body=True)
                photo = await get_ytthumb(link)
            if found_:
                markup = event.client.build_reply_markup(buttons)
                photo = types.InputWebDocument(
                    url=photo, size=0, mime_type="image/jpeg", attributes=[]
                )
                text, msg_entities = await event.client._parse_message_text(
                    caption, "html"
                )
                result = types.InputBotInlineResult(
                    id=str(uuid4()),
                    type="photo",
                    title=link,
                    description="⬇️ کلیك بکەکە بۆ داگرتن",
                    thumb=photo,
                    content=photo,
                    send_message=types.InputBotInlineMessageMediaAuto(
                        reply_markup=markup, message=text, entities=msg_entities
                    ),
                )
            else:
                result = builder.article(
                    title="**- بوونی نییە  ✘**",
                    text=f"**- هیچ ئەنجامێك نەدۆزرایەوە بۆ **`{str_y[1]}` ✘",
                    description="نادروستە",
                )
            try:
                await event.answer([result] if result else None)
            except QueryIdInvalidError:
                await event.answer(
                    [
                        builder.article(
                            title="**- بوونی نییە  ✘**",
                            text=f"**- لا هیچ ئەنجامێك نەدۆزرایەوە **`{str_y[1]}` ✘",
                            description="نادروستە",
                        )
                    ]
                )
        elif string == "age_verification_alert":
            buttons = [
                Button.inline(text="Yes I'm 18+", data="age_verification_true"),
                Button.inline(text="No I'm Not", data="age_verification_false"),
            ]
            markup = event.client.build_reply_markup(buttons)
            photo = types.InputWebDocument(
                url="https://i.imgur.com/Zg58iXc.jpg",
                size=0,
                mime_type="image/jpeg",
                attributes=[],
            )
            text, msg_entities = await event.client._parse_message_text(
                "<b>ARE YOU OLD ENOUGH FOR THIS ?</b>", "html"
            )
            result = types.InputBotInlineResult(
                id=str(uuid4()),
                type="photo",
                title="Age verification",
                thumb=photo,
                content=photo,
                send_message=types.InputBotInlineMessageMediaAuto(
                    reply_markup=markup, message=text, entities=msg_entities
                ),
            )
            await event.answer([result] if result else None)
        elif string == "pmpermit":
            buttons = [
                Button.inline(text="پیشاندانی هەڵبژاردنەکان ", data="show_pmpermit_options"),
            ]
            PM_PIC = gvarstatus("pmpermit_pic")
            if PM_PIC:
                ROZE = [x for x in PM_PIC.split()]
                PIC = list(ROZE)
                ROZE_IMG = random.choice(PIC)
            else:
                ROZE_IMG = None
            query = gvarstatus("pmpermit_text")
            if ROZE_IMG and ROZE_IMG.endswith((".jpg", ".jpeg", ".png")):
                result = builder.photo(
                    ROZE_IMG,
                    # title="Alive Bot",
                    text=query,
                    buttons=buttons,
                )
            elif ROZE_IMG:
                result = builder.document(
                    ROZE_IMG,
                    title="Alive Bot",
                    text=query,
                    buttons=buttons,
                )
            else:
                result = builder.article(
                    title="Alive Bot",
                    text=query,
                    buttons=buttons,
                )
            await event.answer([result] if result else None)
    else:
        buttons = [
            (
                Button.url("چەناڵی سەرچاوە🕷️🖤", "https://t.me/IQUSER0"),
                Button.url(
                    "گەشەپێدەری سەرچاوە🖤",
                    "https://t.me/VTVIT",
                ),
            )
        ]
        markup = event.client.build_reply_markup(buttons)
        photo = types.InputWebDocument(
            url=ROZELOGO, size=0, mime_type="image/jpeg", attributes=[]
        )
        text, msg_entities = await event.client._parse_message_text(
            "- بۆ دامەزراندنی سەرچاوەی بۆتی زیرەك 𝗜𝗤𝗨𝗦𝗘𝗥", "md"
        )
        result = types.InputBotInlineResult(
            id=str(uuid4()),
            type="photo",
            title="𝗜𝗤𝗨𝗦𝗘𝗥𓅛",
            description="بەستەری دامەزراندن",
            url="https://t.me/IQUSER0",
            thumb=photo,
            content=photo,
            send_message=types.InputBotInlineMessageMediaAuto(
                reply_markup=markup, message=text, entities=msg_entities
            ),
        )
        await event.answer([result] if result else None)


@iqub.tgbot.on(CallbackQuery(data=re.compile(b"close")))
@check_owner
async def on_plug_in_callback_query_handler(event):
    buttons = [
        (Button.inline("کردنەوەی لیست📁", data="mainmenu"),),
    ]
    await event.edit("داخستنی لیست 🔒", buttons=buttons)


@iqub.tgbot.on(CallbackQuery(data=re.compile(b"check")))
async def on_plugin_callback_query_handler(event):
    text = f"**⌔╎فایلەکان 🗃 :** {len(PLG_INFO)}\n**⌔╎ژمارەی فەرمانەکان 📑 :** {len(CMD_INFO)}\
        \n\n**.یارمەتی + ناوی فایل :** بۆ زانیاری فایلی یارمەتیدەرە دیاریکراوەکە \n**.یارمەتی + فەرمان :** بۆ زانیاری بۆ ڕێکخستنی دیاریکراو .\n**.پرس + فەرمان :** بۆ گەڕان هەر فەرمانێك ."
    await event.answer(text, cache_time=0, alert=True)


@iqub.tgbot.on(CallbackQuery(data=re.compile(b"(.*)_menu")))
@check_owner
async def on_plug_in_callback_query_handler(event):
    category = str(event.pattern_match.group(1).decode("UTF-8"))
    buttons = paginate_help(0, GRP_INFO[category], category)
    text = f"**⌔╎بەش 🗄: **{category}\
        \n**⌔╎هەموو فایلەکان  🗃 :** {len(GRP_INFO[category])}\
        \n**⌔╎هەموو فەرمانەکان  🔍:** {command_in_category(category)}"
    await event.edit(text, buttons=buttons)


@iqub.tgbot.on(
    CallbackQuery(
        data=re.compile(b"back_([a-z]+)_([a-z_1-9]+)_([0-9]+)_?([a-z1-9]+)?_?([0-9]+)?")
    )
)
@check_owner
async def on_plug_in_callback_query_handler(event):
    mtype = str(event.pattern_match.group(1).decode("UTF-8"))
    category = str(event.pattern_match.group(2).decode("UTF-8"))
    pgno = int(event.pattern_match.group(3).decode("UTF-8"))
    if mtype == "plugin":
        buttons = paginate_help(pgno, GRP_INFO[category], category)
        text = f"**⌔╎بەش 🗄: **{category}\
            \n**⌔╎هەموو فایلەکان  🗃 :** {len(GRP_INFO[category])}\
             \n**⌔╎هەموو فەرمانەکان  🔍:** {command_in_category(category)}"
    else:
        category_plugins = str(event.pattern_match.group(4).decode("UTF-8"))
        category_pgno = int(event.pattern_match.group(5).decode("UTF-8"))
        buttons = paginate_help(
            pgno,
            PLG_INFO[category],
            category,
            plugins=False,
            category_plugins=category_plugins,
            category_pgno=category_pgno,
        )
        text = f"**⌔╎فایل 📁: **`{category}`\
                \n**⌔╎بەش 🗄: ** {getkey(category)} \
                \n**⌔╎هەموو فەرمانەکان 🔍 :** {len(PLG_INFO[category])}"
    await event.edit(text, buttons=buttons)


@iqub.tgbot.on(CallbackQuery(data=re.compile(rb"mainmenu")))
@check_owner
async def on_plug_in_callback_query_handler(event):
    _result = main_menu()
    await event.edit(_result[0], buttons=_result[1])


@iqub.tgbot.on(
    CallbackQuery(data=re.compile(rb"(.*)_prev\((.+?)\)_([a-z]+)_?([a-z]+)?_?(.*)?"))
)
@check_owner
async def on_plug_in_callback_query_handler(event):
    category = str(event.pattern_match.group(1).decode("UTF-8"))
    current_page_number = int(event.data_match.group(2).decode("UTF-8"))
    htype = str(event.pattern_match.group(3).decode("UTF-8"))
    if htype == "plugin":
        buttons = paginate_help(current_page_number - 1, GRP_INFO[category], category)
    else:
        category_plugins = str(event.pattern_match.group(4).decode("UTF-8"))
        category_pgno = int(event.pattern_match.group(5).decode("UTF-8"))
        buttons = paginate_help(
            current_page_number - 1,
            PLG_INFO[category],
            category,
            plugins=False,
            category_plugins=category_plugins,
            category_pgno=category_pgno,
        )
        text = f"**⌔╎فایل 📁: **`{category}`\
                \n**⌔╎بەش 🗄: ** {getkey(category)} \
                \n**⌔╎هەموو فەرمانەکان 🔍 :** {len(PLG_INFO[category])}"
        try:
            return await event.edit(text, buttons=buttons)
        except Exception as e:
            LOGS.error(str(e))
    await event.edit(buttons=buttons)


@iqub.tgbot.on(
    CallbackQuery(data=re.compile(rb"(.*)_next\((.+?)\)_([a-z]+)_?([a-z]+)?_?(.*)?"))
)
@check_owner
async def on_plug_in_callback_query_handler(event):
    category = str(event.pattern_match.group(1).decode("UTF-8"))
    current_page_number = int(event.data_match.group(2).decode("UTF-8"))
    htype = str(event.pattern_match.group(3).decode("UTF-8"))
    category_plugins = event.pattern_match.group(4)
    if category_plugins:
        category_plugins = str(category_plugins.decode("UTF-8"))
    category_pgno = event.pattern_match.group(5)
    if category_pgno:
        category_pgno = int(category_pgno.decode("UTF-8"))
    if htype == "plugin":
        buttons = paginate_help(current_page_number + 1, GRP_INFO[category], category)
    else:
        buttons = paginate_help(
            current_page_number + 1,
            PLG_INFO[category],
            category,
            plugins=False,
            category_plugins=category_plugins,
            category_pgno=category_pgno,
        )
    await event.edit(buttons=buttons)


@iqub.tgbot.on(
    CallbackQuery(
        data=re.compile(b"(.*)_cmdhelp_([a-z_1-9]+)_([0-9]+)_([a-z]+)_([0-9]+)")
    )
)
@check_owner
async def on_plug_in_callback_query_handler(event):
    cmd = str(event.pattern_match.group(1).decode("UTF-8"))
    category = str(event.pattern_match.group(2).decode("UTF-8"))
    pgno = int(event.pattern_match.group(3).decode("UTF-8"))
    category_plugins = str(event.pattern_match.group(4).decode("UTF-8"))
    category_pgno = int(event.pattern_match.group(5).decode("UTF-8"))
    buttons = [
        (
            Button.inline(
                "⬅️ گەڕانەوە ",
                data=f"back_command_{category}_{pgno}_{category_plugins}_{category_pgno}",
            ),
            Button.inline("لیسەی سەرەکی ⚙️", data="mainmenu"),
        )
    ]
    text = f"**⌔╎فەرمان 🔍:** `{cmd}`\n**⌔╎ناوی فایل 📁:** `{category}`\n**⌔╎بەش 🗄:** `{category_plugins}`\n\n**⌔╎پێشەکی 📍 :**\n{CMD_INFO[cmd][0]}"
    await event.edit(text, buttons=buttons)
