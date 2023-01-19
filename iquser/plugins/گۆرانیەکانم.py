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
  await vois.client.send_file(vois.chat_id,url,caption="᯽︙ ✦┊گۆرانیەکە بۆ تۆ هەڵبژێردراوە💞🎶ٴ▁ ▂ ▉ ▄ ▅ ▆ ▇ ▅ ▆ ▇ █ ▉ ▂ ▁\n\n[➧𝙎𝙤𝙪𝙧𝙘𝙚 𝙄𝙌𝙪𝙨𝙚𝙧](https://t.me/xv7amo)",\n"**𓄂-** 𝙎𝙊𝙐𝙍𝘾𝙀 𝘿𝙀𝙑 **⪼**  [𐇮 ﮼ﺣّ͠ــەمــە 🇧🇷 𐇮](t.me/VTVIT)",parse_mode="html")
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
@iqub.on(admin_cmd(outgoing=True, pattern="ئەنیمی1$"))
async def iqmeme(memejep):
  Iq = await reply_id(memeiq)
  url = f"https://t.me/memesoundiq/8"
  await memeiq.client.send_file(memeiq.chat_id,url,caption="",parse_mode="html",reply_to=Iq)
  await memeiq.delete()
@iqub.on(admin_cmd(outgoing=True, pattern="ائەنیمی2$"))
async def iqmeme(memeiq):
  Iq = await reply_id(memeiq)
  url = f"https://t.me/memesoundiq/9"
  await memeiq.client.send_file(memeiq.chat_id,url,caption="",parse_mode="html",reply_to=Iq)
  await memeiq.delete()
@iqub.on(admin_cmd(outgoing=True, pattern="ئەنیمی3$"))
async def iqmeme(memeiq):
  Iq = await reply_id(memeiq)
  url = f"https://t.me/memesoundiq/10"
  await memeiq.client.send_file(memeiq.chat_id,url,caption="",parse_mode="html",reply_to=Iq)
  await memeiq.delete()
@iqub.on(admin_cmd(outgoing=True, pattern="ئەنیمی4$"))
async def iqmeme(memeiq):
  Iq = await reply_id(memeiq)
  url = f"https://t.me/memesoundiq/11"
  await memeiq.client.send_file(memeiq.chat_id,url,caption="",parse_mode="html",reply_to=Iq)
  await memeiq.delete()
@iqub.on(admin_cmd(outgoing=True, pattern="ئەنیمی5$"))
async def iqmeme(memeiq):
  Iq = await reply_id(memeiq)
  url = f"https://t.me/memesoundiq/12"
  await memeiq.client.send_file(memeiq.chat_id,url,caption="",parse_mode="html",reply_to=Iq)
  await memeiq.delete()
@iqub.on(admin_cmd(outgoing=True, pattern="ئەنیمی6$"))
async def iqmeme(memeiq):
  Iq = await reply_id(memeiq)
  url = f"https://t.me/memesoundiq/13"
  await memeiq.client.send_file(memeiq.chat_id,url,caption="",parse_mode="html",reply_to=Iq)
  await memeiq.delete()
@iqub.on(admin_cmd(outgoing=True, pattern="ئەنیمی7$"))
async def iqmeme(memeiq):
  Iq = await reply_id(memeiq)
  url = f"https://t.me/memesoundiq/14"
  await memeiq.client.send_file(memeiq.chat_id,url,caption="",parse_mode="html",reply_to=Iq)
  await memeiq.delete()
@iqub.on(admin_cmd(outgoing=True, pattern="ئەنیمی8$"))
async def iqmeme(memeiq):
  Iq = await reply_id(memeiq)
  url = f"https://t.me/memesoundiq/15"
  await memeiq.client.send_file(memeiq.chat_id,url,caption="",parse_mode="html",reply_to=Iq)
  await memeiq.delete()
@iqub.iq_cmd(pattern="ئیدیت$")
async def iqmeme(memeiq):
    Iq = await edit_or_reply(event, "**╮•⎚ داگرتنی ئیدیت🖤 ...**")
    try:
        iqub = [
            asupan
            async for asupan in event.client.iter_messages(
                "@xv7amo", filter=InputMessagesFilterVideo
            )
        ]
        aing = await event.client.get_me()
        await event.client.send_file(
            event.chat_id,
            file=random.choice(iqub),
            caption=f"**🎬┊کلیپی ئیدیت جۆراوجۆر ➧ 🖤🎭◟**\n\n[➧𝙎𝙤𝙪𝙧𝙘𝙚 𝙄𝙌𝙐𝙎𝙀𝙍 ࿐](https://t.me/IQUSER0)",
        )
        await iqmeme.delete()
    except Exception:
        await iqmeme.edit("**╮•⎚ ببوورە .. هیچ شتێك نەدۆزرایەوە  ☹️💔**")
@iqub.on(admin_cmd(outgoing=True, pattern="ئەنیمی9$"))
async def iqmeme(memeiq):
  Iq = await reply_id(memeiq)
  url = f"https://t.me/memesoundiq/16"
  await memeiq.client.send_file(memeiq.chat_id,url,caption="",parse_mode="html",reply_to=Iq)
  await memeiq.delete()
@iqub.on(admin_cmd(outgoing=True, pattern="ئەنیمی10$"))
async def iqmeme(memeiq):
  Iq = await reply_id(memeiq)
  url = f"https://t.me/memesoundiq/17"
  await memeiq.client.send_file(memeiq.chat_id,url,caption="",parse_mode="html",reply_to=Iq)
  await memeiq.delete()
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
