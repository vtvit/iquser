import asyncio
import random
from asyncio.exceptions import TimeoutError

from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError

from iquser import iqub
from ..helpers.utils import reply_id

# کۆپی مکاا
@iqub.on(admin_cmd(pattern="دۆخی ئەکاونت ?(.*)"))
async def _(event):
    await event.edit("**-دۆخی تۆ دەپشکنرێت ئەگەر تۆ قەدەغەکراویت یان نا**")
    async with bot.conversation("@SpamBot") as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=178220800)
            )
            await conv.send_message("/start")
            response = await response
            await bot.send_read_acknowledge(conv.chat_id)
        except YouBlockedUserError:
            await event.edit("** ییەکەم جار لادانی بلۆک @SpamBot دواتر هەوڵبدە **")
            return
        await event.edit(f"- {response.message.message}\n @xv7amo")


@iqub.on(admin_cmd(pattern="گەڕانی گۆرانی ?(.*)"))
async def _(event):
    "To reverse search music by bot."
    if not event.reply_to_msg_id:
        return await event.edit("**▾∮ پێویستە وەڵامی گۆرانیەکە بدەیتەوە سەرەتا**")
    reply_message = await event.get_reply_message()
    chat = "@auddbot"
    try:
        async with event.client.conversation(chat) as conv:
            try:
                await event.edit("**▾∮ گۆرانیەکە دەناسرێتەوە کەمێك چاوەڕێ بکە**")
                start_msg = await conv.send_message("/start")
                response = await conv.get_response()
                send_audio = await conv.send_message(reply_message)
                check = await conv.get_response()
                if not check.text.startswith("Audio received"):
                    return await event.edit(
                        "**▾∮ پێویستە درێژی گۆرانیەکە 5 بۆ 10 چرکە بێت **."
                    )
                await event.edit("- کەمێك چاوەڕێ بکە")
                result = await conv.get_response()
                await event.client.send_read_acknowledge(conv.chat_id)
            except YouBlockedUserError:
                await event.edit("```Mohon buka blokir (@auddbot) dan coba lagi```")
                return
            namem = f"**گۆرانی : **{result.text.splitlines()[0]}\
        \n\n**وردەکاری : **{result.text.splitlines()[2]}"
            await event.edit(namem)
            await event.client.delete_messages(
                conv.chat_id,
                [start_msg.id, send_audio.id, check.id, result.id, response.id],
            )
    except TimeoutError:
        return await event.edit("***هەڵەیەك ڕوویدا دووبارە هەوڵ بدە**")


@iqub.on(admin_cmd(pattern="جیمێڵی ساختە(?: |$)(.*)"))
async def _(event):
    chat = "@TempMailBot"
    geez = await event.edit("**دروست دەکرێت ...**")
    async with bot.conversation(chat) as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=220112646)
            )
            await conv.send_message("/start")
            await asyncio.sleep(1)
            await conv.send_message("/create")
            response = await response
            jepiqmail = (response).reply_markup.rows[2].buttons[0].url
            await event.client.send_read_acknowledge(conv.chat_id)
        except YouBlockedUserError:
            await geez.edit("**بلۆکی لابدە  @TempMailBot وە هەوڵبدەوە دووبارە**")
            return
        await event.edit(
            f"ئەمە جیمێڵی تایبەت بەتۆیە `{response.message.message}`\n[ ئێرە دابگرە بۆ بینینی نامەکانی جیمێڵەکە]({iqubgmail})"
        )
@iqub.on(admin_cmd(outgoing=True, pattern="گۆرانیەکانم$"))
async def iqvois(vois):
  rl = random.randint(3,267)
  url = f"https://t.me/IQMUC/{rl}"
  await vois.client.send_file(vois.chat_id,url,caption="᯽︙ BY : @VTVIT 👾",parse_mode="html")
  await vois.delete()

@iqub.on(admin_cmd(outgoing=True, pattern="شعر$"))
async def iqvois(vois):
  rl = random.randint(2,101)
  url = f"https://t.me/L1BBBL/{rl}"
  await vois.client.send_file(vois.chat_id,url,caption="᯽︙ BY : @xv7amo 👾",parse_mode="html")
  await vois.delete()
@iqub.on(admin_cmd(outgoing=True, pattern="قورئان$"))
async def iqvois(vois):
  rl = random.randint(2,101)
  url = f"https://t.me/IQQUR/{rl}"
  await vois.client.send_file(vois.chat_id,url,caption="᯽︙ BY : @IQUSER0E 🤲🏻☪️",parse_mode="html")
  await vois.delete()
@iqub.on(admin_cmd(outgoing=True, pattern="هەڵە مەکە$"))
async def iqmeme(memeiq):
  Iq = await reply_id(memeiq)
  url = f"https://t.me/memesoundiq/7"
  await memeiq.client.send_file(memeiq.chat_id,url,caption="",parse_mode="html",reply_to=Iq)
  await memeiq.delete()
@iqub.on(admin_cmd(outgoing=True, pattern="گاڵتە$"))
async def iqmeme(memeiq):
  Iq = await reply_id(memeiq)
  url = f"https://t.me/memesoundiq/6"
  await memeiq.client.send_file(memeiq.chat_id,url,caption="",parse_mode="html",reply_to=Iq)
  await memeiq.delete()
@iqub.on(admin_cmd(outgoing=True, pattern="خودا$"))
async def iqmeme(memeiq):
  Iq = await reply_id(memeiq)
  url = f"https://t.me/memesoundiq/4"
  await memeiq.client.send_file(memeiq.chat_id,url,caption="",parse_mode="html",reply_to=Iq)
  await memeiq.delete()
@jepiq.on(admin_cmd(outgoing=True, pattern="انمي1$"))
async def jepmeme(memejep):
  Jep = await reply_id(memejep)
  url = f"https://t.me/MemeSoundJep/7"
  await memejep.client.send_file(memejep.chat_id,url,caption="",parse_mode="html",reply_to=Jep)
  await memejep.delete()
@jepiq.on(admin_cmd(outgoing=True, pattern="انمي2$"))
async def jepmeme(memejep):
  Jep = await reply_id(memejep)
  url = f"https://t.me/MemeSoundJep/9"
  await memejep.client.send_file(memejep.chat_id,url,caption="",parse_mode="html",reply_to=Jep)
  await memejep.delete()
@jepiq.on(admin_cmd(outgoing=True, pattern="انمي3$"))
async def jepmeme(memejep):
  Jep = await reply_id(memejep)
  url = f"https://t.me/MemeSoundJep/11"
  await memejep.client.send_file(memejep.chat_id,url,caption="",parse_mode="html",reply_to=Jep)
  await memejep.delete()
@jepiq.on(admin_cmd(outgoing=True, pattern="انمي4$"))
async def jepmeme(memejep):
  Jep = await reply_id(memejep)
  url = f"https://t.me/MemeSoundJep/12"
  await memejep.client.send_file(memejep.chat_id,url,caption="",parse_mode="html",reply_to=Jep)
  await memejep.delete()
@jepiq.on(admin_cmd(outgoing=True, pattern="انمي5$"))
async def jepmeme(memejep):
  Jep = await reply_id(memejep)
  url = f"https://t.me/MemeSoundJep/13"
  await memejep.client.send_file(memejep.chat_id,url,caption="",parse_mode="html",reply_to=Jep)
  await memejep.delete()
@jepiq.on(admin_cmd(outgoing=True, pattern="انمي6$"))
async def jepmeme(memejep):
  Jep = await reply_id(memejep)
  url = f"https://t.me/MemeSoundJep/14"
  await memejep.client.send_file(memejep.chat_id,url,caption="",parse_mode="html",reply_to=Jep)
  await memejep.delete()
@jepiq.on(admin_cmd(outgoing=True, pattern="انمي7$"))
async def jepmeme(memejep):
  Jep = await reply_id(memejep)
  url = f"https://t.me/MemeSoundJep/15"
  await memejep.client.send_file(memejep.chat_id,url,caption="",parse_mode="html",reply_to=Jep)
  await memejep.delete()
@jepiq.on(admin_cmd(outgoing=True, pattern="انمي8$"))
async def jepmeme(memejep):
  Jep = await reply_id(memejep)
  url = f"https://t.me/MemeSoundJep/16"
  await memejep.client.send_file(memejep.chat_id,url,caption="",parse_mode="html",reply_to=Jep)
  await memejep.delete()
@jepiq.on(admin_cmd(outgoing=True, pattern="انمي9$"))
async def jepmeme(memejep):
  Jep = await reply_id(memejep)
  url = f"https://t.me/MemeSoundJep/17"
  await memejep.client.send_file(memejep.chat_id,url,caption="",parse_mode="html",reply_to=Jep)
  await memejep.delete()
@iqub.on(admin_cmd(outgoing=True, pattern="انمي10$"))
async def jepmeme(memejep):
  Iq = await reply_id(memejep)
  url = f"https://t.me/MemeSoundJep/18"
  await memejep.client.send_file(memejep.chat_id,url,caption="",parse_mode="html",reply_to=Jep)
  await memejep.delete()
@iqub.on(admin_cmd(outgoing=True, pattern="جڕت2$"))
async def iqmeme(memeiq):
  Iq = await reply_id(memeiq)
  url = f"https://t.me/memesoundiq/3"
  await memeiq.client.send_file(memeiq.chat_id,url,caption="",parse_mode="html",reply_to=Iq)
  await memeiq.delete()
@iqub.on(admin_cmd(outgoing=True, pattern="جڕت$"))
async def iqmeme(memeiq):
  Iq = await reply_id(memeiq)
  url = f"https://t.me/memesoundiq/2"
  await memeiq.client.send_file(memeiq.chat_id,url,caption="",parse_mode="html",reply_to=Iq)
  await memeiq.delete()
