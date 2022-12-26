#   هەموو مافەکان بۆ سەرچاوەی گەشەپێدەرانی بۆتی زیرەك تەنها بۆ ئەوانن
#   ئەگەر فایلەکە بەو مافانە بڕووخێنیت و نووسەر و گەشەپێدەرەکانی مافەکان بسڕنەوە و ببن بە شکست 👍
#    نوسینی محمد 
import asyncio
import io
import re

from telethon import Button, custom, events
from telethon.tl.functions.users import GetFullUserRequest
from iquser import iqub
from iquser.sql_helper.blacklist_assistant import (
    add_nibba_in_db,
    is_he_added,
    removenibba,
)
from iquser.sql_helper.botusers_sql import add_me_in_db, his_userid
from iquser.sql_helper.idadder_sql import (
    add_usersid_in_db,
    already_added,
    get_all_users,
)
from iqub.razan.resources.assistant import *
#start 
@tgbot.on(events.NewMessage(pattern="^/start"))
async def start(event):
    rehu = await tgbot.get_me()
    bot_id = rehu.first_name
    bot_username = rehu.username
    replied_user = await event.client(GetFullUserRequest(event.sender_id))
    firstname = replied_user.users[0].first_name
    vent = event.chat_id
    starttext = f"**سڵاو {firstname} ! من {bot_id}, بۆتێکی سادەیی یارمەتیدەرم 🧸🤍 \n\n- [خاوەن بۆت](tg://user?id={bot.uid}) \nدەتوانیت لە ڕێگەی ئەم بۆتەوە پەیام بە خاوەنەکە بدەیت  . \n\nئەگەر دەتەوێت بۆتەکەی خۆت دابمەزرێنیت، دوگمەکانی خوارەوە بپشکنە**"
    if event.sender_id == bot.uid:
        await tgbot.send_message(
            vent,
            message=f"بەخێربێیت بەڕێزم، 🖤 {bot_id}, یاریدەدەر ! \nئەمڕۆ دەتەوێت چی بکەیت ?",
            buttons=[
                                     [Button.inline("پیشاندانی بەکارهێنەران 📬", data="users"), Button.inline(
                                         "فەرمانەکانی بۆت ⚒️", data="gibcmd")],
                                     [Button.url("گەشەپێدەر 🔗", "https://t.me/IQ7amo"), Button.inline(
                                         "فەرمانی زەخرەفە", data="rozzag")],

                                 ])
    else:
        if already_added(event.sender_id):
            pass
        elif not already_added(event.sender_id):
            add_usersid_in_db(event.sender_id)
        await tgbot.send_message(
            event.chat_id,
            message=starttext,
            link_preview=False,
            buttons=[
                [custom.Button.inline("دامەزراندنی بۆتی زیرەك  🕷️", data="deploy")],
                [Button.url("پێویستیت بە یارمەتییە ❓", "https://t.me/IQ7amo")],
            ],
        )

#Data

@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"deploy")))
async def help(event):
    await event.delete()
    if event.query.user_id is not bot.uid:
        await tgbot.send_message(
            event.chat_id,
            message="**بۆ دامەزراندنی بۆتەکەت هەنگاوەکانی خوارەوە پەیڕەو بکە هەوڵبدە و ئەگەر ناتوانیت بچیت بۆ گروپی یارمەتیدان بۆ یارمەتیدانت 🧸♥ **.",
            buttons=[
                [Button.url("ڕوونکردنەوەی دامەزراندن 🕷️", "https://t.me/VTVIT")],
                [Button.url("گرووپی یارمەتیدەر ❓", "https://t.me/GroupIQuser")],
            ],
        )


@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"users")))
async def users(event):
    if event.query.user_id == bot.uid:
        await event.delete()
        total_users = get_all_users()
        users_list = "- لیستی بەکارهێنەرانی بۆت  : \n\n"
        for starked in total_users:
            users_list += ("==> {} \n").format(int(starked.chat_id))
        with io.BytesIO(str.encode(users_list)) as tedt_file:
            tedt_file.name = "jepthon.txt"
            await tgbot.send_file(
                event.chat_id,
                tedt_file,
                force_document=True,
                caption="هەموو بەکارهێنەرانی بۆت",
                allow_cache=False,
            )
    else:
        pass


@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"gibcmd")))
async def users(event):
    await event.delete()
    rorza = "**لـیـسـتـی فـەرمـانـەکانی بـۆتی تـایـبـەت بـەتۆ🕷️🖤.**:\n- **هەموو ئەم فەرمانانە بەکاردێن دوای زیادکردنی بۆتەکە لە گروپێکدا و بەرزکردنەوەی بۆ بەڕێوبەر بە هەندێك هێزەوە‌🕷️🖤. **\n• /start \n (بۆ دڵنیابوون لە دۆخی بۆت🕷️🖤.) \n• /ping \n (فەرمانی پینگ🕷️🖤.)  \n• /broadcast \n (بۆ دروستکردنی ڕادیۆیەك بۆ هەموو بەکارهێنەران لە بۆتێکدا🕷️🖤.)  \n• /id \n  (بۆ بینینی ناسنامەی کەسێك🕷️🖤.) \n• /alive \n- (بۆ بینینی زانیاری بۆتەکە🕷️🖤.) \n• /bun \n-  (بۆ دەرکردنی کەسێك لە گرووپ بەکاردێت🕷️🖤.)\n• /unbun  \n-  (بۆ لادانی دەرکردن لە گرووپ بەکاردێت🕷️🖤.)  \n• /prumote  \n-  (بۆ بەرزکردنەوەی کەسەکە لە پلەی بەڕێوبەری🕷️🖤.)\n• /demute  \n-  (بۆ دابەزاندنی کەسەکە لە پلەی بەڕێوبەری🕷️🖤.) \n• /pin  \n-  (بۆ هەڵواسینی نامە لە گرووپ🕷️🖤.)  \n• /stats  \n-  (بۆ بینینی بەکارهێنەرانی بۆت🕷️🖤.)  \n• /purge \n- (بە وەڵامدانەوەی نامەیەك بۆ سڕینەوەی نامەکانی خوارەوەی🕷️🖤.) \n• /del  \n-  (بە وەڵامدانەوەی نامەکە بۆ سڕینەوەی🕷️🖤.)"
    await tgbot.send_message(event.chat_id, rorza)


@tgbot.on(events.NewMessage(pattern="^/help", func=lambda e: e.sender_id == bot.uid))
async def starkislub(event):
    rorza = "**لـیـسـتی فـەرمـانـەکـانی بـۆتی تـایـبـەت بـە تۆ🕷️🖤.**:\n- ** هەموو ئەم فەرمانانە بەکاردێن دوای زیادکردنی بۆتەکە لە گروپێکدا و بەرزکردنەوەی بۆ بەڕێوبەر بە هەندێك هێزەوە‌🕷️🖤. **\n• /start \n (بۆ دڵنیابوون لە دۆخی بۆت🕷️🖤.) \n• /ping \n (فەرمانی پینگ🕷️🖤.)  \n• /broadcast \n ( \n• /broadcast \n (بۆ دروستکردنی ڕادیۆیەك بۆ هەموو بەکارهێنەران لە بۆتێکدا🕷️🖤.)  \n• /id \n  (بۆ بینینی ناسنامەی کەسێك🕷️🖤.) \n• /alive \n- (بۆ بینینی زانیاری بۆتەکە🕷️🖤.) \n• /bun \n-  (ۆ دەرکردنی کەسێك لە گرووپ بەکاردێت🕷️🖤.)\n• /unbun  \n-  (بۆ لادانی دەرکردن لە گرووپ بەکاردێت🕷️🖤.)  \n• /prumote  \n-  (بۆ بەرزکردنەوەی کەسەکە لە پلەی بەڕێوبەری🕷️🖤.)\n• /demute  \n-  (بۆ دابەزاندنی کەسەکە لە پلەی بەڕێوبەری🕷️🖤.) \n• /pin  \n-  (بۆ هەڵواسینی نامە لە گرووپ🕷️🖤.)  \n• /stats  \n-  (بۆ بینینی بەکارهێنەرانی بۆت🕷️🖤.)  \n• /purge  \n-  (بە وەڵامدانەوەی نامەیەك بۆ سڕینەوەی نامەکانی خوارەوەی🕷️🖤.) \n• /del  \n-  (بە وەڵامدانەوەی نامەکە بۆ سڕینەوەی🕷️🖤.)"
    await event.reply(rorza)

@tgbot.on(events.NewMessage(pattern="^/alive", func=lambda e: e.sender_id == bot.uid))
async def starkislub(event):
    razan = "**𝙄𝙌𝙐𝙎𝙀𝙍 メ**\n•━═━═━═━═━━═━═━═━═━•‌‌\n**- دۆخی بۆت ** سەرکەوتووان کاردەکات\n**- وەشانی تێلثۆن  **: 1.23.0\n**- وەشانی پایثۆن **: 3.9.6\n**- ناوی بەکارهێنەر ** {mention}\n**- CH : @xv7amo\n•━═━═━═━═━━═━═━═━═━•‌‌\n"
    await event.reply(razan)
    
    


"""  مافەکانم، شەرەفی تۆ ئەوەیە شتێک بگۆڕیت کە بە شەرەفی خۆت یاری بکەیت """

# بـەنـاوی خـودای گـەورە و مـیـھـرەبـان🤍🍀
# داوای لێخۆشبوون لەخوا دەکەم لەکاتێکدا تۆ خۆت فایلەکان دەبەیت 🖤، 
@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"rozzag"))) 
async def settings(event):
    if event.sender_id == bot.uid:
        await event.delete()
        await tgbot.send_message(event.chat_id,
                                 "**⌯︙ یەکێك لەمانەی خوارەوە هەڵبژێرە🌿💓. : **",
                                 buttons=[
                                 [Button.inline(
                                     "ناوی ئینگلیزی َِ🛹🖤", data="rozname"),
                                  Button.inline(
                                     "بایۆ َِ🛹🖤", data="rozpio1")],
                                 [Button.inline(
                                     "ناوی مانگەکان َِ🛹🖤", data="rozmonth"),
                                  Button.inline(
                                     "ناوی چەناڵەکان َِ🛹‌🖤", data="chanlan")]
                                 ])
    else:
        await event.answer("تۆ ناتوانیت بۆت بکاربهێنیت🌿💓. @xv7amo", alert=True)




@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"rozname"))) 
async def settings(event):  #    بـەشـی زەخـرەفـەی بـۆتـی زیـرەك🕷️🖤
    if event.sender_id == bot.uid:
        await event.delete()
        await tgbot.send_message(event.chat_id,
                                 "**⌯︙ یەکێك لەمانەی خوارەوە هەڵبژێرە🌿💓. **",
                                 buttons=[
                                     [Button.inline(
                                         "ناوی کوڕان َِ🖤", data="razan"),
                                      Button.inline(
                                         "ناوی کچان َِ🖤", data="RR7PP"),
                                      Button.inline(
                                         "║ گەڕانەوە🕷️ ║ ⁦⁩", data="rozzag")]
                                 ])
    else:
        await event.answer("تۆ ناتوانیت بۆت بەکاربهێنیت🌿. @xv7amo", alert=True)


@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"razan")))  
async def settings(event):  #    بـەشـی زەخـرەفـەی نـاوی کـوڕان
    if event.sender_id == bot.uid:
        await event.delete()
        await tgbot.send_message(event.chat_id,
                                 "**⌯︙ یەکێك لەمانەی خوارەوە هەڵبژێرە🌿💓. **",
                                 buttons=[
                                     [Button.inline(
                                         "لیستی یەکەم َِ🛹🖤", data="rzan1"),
                                      Button.inline(
                                         "لیستی دووەم َِ🛹🖤", data="raza2")],
                                     [Button.inline(
                                         "║ گەڕانەوە🕷️ ║", data="rozname")]
                                 ])
    else:
        await event.answer("تۆ ناتوانیت بۆت بەکاربهێنیت🌿. @xv7amo", alert=True)



# Boys zag list1 - لـیـستی یـەکـەمی نـاوی کوڕان
@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"rzan1")))
async def settings(event): #    بـەشـی زەخـرەفـەی نـاوی کوڕان 1
    if event.sender_id == bot.uid:
        await event.delete()
        await tgbot.send_message(event.chat_id,
                                 Boyroz1, 
                                 buttons=[[Button.inline("║ گەڕانەوە🕷️ ║", data="razan")]
                                 ])
    else:
        await event.answer("تۆ ناتوانیت ئەم بۆتە بەکاربهێنیت🌿.", alert=True)


# Boys zag list2 - لـیـستـی دووەمـی نـاوی کوڕان
@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"raza2"))) 
async def settings(event):  #    بـەشـی زەخـرەفـەی نـاوی کوڕان 2
    if event.sender_id == bot.uid:
        await event.delete()
        await tgbot.send_message(event.chat_id,
                                 Boyroz2, 
                                 buttons=[[Button.inline("║ گەڕانەوە🕷️ ║", data="razan")]
                                 ])
    else:
        await event.answer("تۆ ناتوانیت ئەم بۆتە بەکاربهێنیت🌿.", alert=True)


@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"RR7PP")))
async def settings(event): #    بـەشـی زەخـرەفـەی نـاوی کـچان
    if event.sender_id == bot.uid:
        await event.delete()
        await tgbot.send_message(event.chat_id,
                                 "**⌯︙ یەکێك لەمانەی خوارەوە هەڵبژێرە🌿💓. **",
                                 buttons=[
                                     [Button.inline(
                                         "لیستی یەکەم َِ🛹🖤", data="RR7PP1"),
                                      Button.inline(
                                         "لیستی دووەم َِ🛹🖤", data="RR7PP2")],
                                     [Button.inline(
                                         "║ گەڕانەوە🕷️ ║", data="rozname")]
                                 ])
    else:
        await event.answer(" تۆ ناتوانیت بۆت بەکاربهێنیت🌿. @xv7amo", alert=True)

# شنو تـدور  :)
@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"RR7PP1")))
async def settings(event): #    بـەشـی زەخـرەفـەی نـاوی کـچان 1
    if event.sender_id == bot.uid:
        await event.delete()
        await tgbot.send_message(event.chat_id,
                                 Girlan1, 
                                 buttons=[[Button.inline("║ گەڕانەوە🕷️ ║", data="RR7PP")]
                                 ])
    else:
        await event.answer("تۆ ناتوانیت ئەم بۆتە بەکاربهێنیت🌿.", alert=True)


@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"RR7PP2")))
async def settings(event):  #    بـەشـی زەخـرەفـەی نـاوی کـچ 2
    if event.sender_id == bot.uid:
        await event.delete()
        await tgbot.send_message(event.chat_id,
                                 Girlan2, 
                                 buttons=[[Button.inline("║ گەڕانەوە🕷️ ║", data="RR7PP")]
                                 ])
    else:
        await event.answer("تۆ ناتوانیت ئەم بۆتە بەکاربهێنیت🌿.", alert=True)

@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"rozpio1"))) 
async def settings(event):  #    بـەشـی بـایـۆ 1
    if event.sender_id == bot.uid:
        await event.delete()
        await tgbot.send_message(event.chat_id,
                                 ROZPIO1,
                                 buttons=[
                                     [Button.inline(
                                         " پێشوو ⫸", data="rozpio5"),
                                      Button.inline(
                                         "║ دەرچوون🕷️ ║ ⁦⁩", data="rozzag"),
                                      Button.inline(
                                         "⫷ دواتر ", data="rozpio2")]
                                 ])
    else:
        await event.answer("تۆ ناتوانیت بۆت بەکاربهێنیت🌿. @xv7amo", alert=True)


@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"rozpio2"))) 
async def settings(event): #    بـەشـی بـایـۆ 2
    if event.sender_id == bot.uid:
        await event.delete()
        await tgbot.send_message(event.chat_id,
                                 ROZPIO2,
                                 buttons=[
                                     [Button.inline(
                                         "پێشوو ⫸ ", data="rozpio1"),
                                      Button.inline(
                                         "║ دەرچوون🕷️ ║ ⁦⁩", data="rozzag"),
                                      Button.inline(
                                         "⫷دواتر ", data="rozpio3")]
                                 ])
    else:
        await event.answer("تۆ ناتوانیت بۆت بەکاربهێنیت🌿. @xv7amo", alert=True)


@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"rozpio3"))) 
async def settings(event): #    بـەشـی بـایـۆ 3
    if event.sender_id == bot.uid:
        await event.delete()
        await tgbot.send_message(event.chat_id,
                                 ROZPIO3,
                                 buttons=[
                                     [Button.inline(
                                         "پێشوو ⫸ ", data="rozpio2"),
                                      Button.inline(
                                         "║ دەرچوون🕷️ ║ ⁦⁩", data="rozzag"),
                                      Button.inline(
                                         "⫷ دواتر", data="rozpio4")]
                                 ])
    else:
        await event.answer("تۆ ناتوانیت بۆت بەکاربهێنیت🌿. @xv7amo", alert=True)


@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"rozpio4"))) 
async def settings(event): #    بـەشـی بـایـۆ 4
    if event.sender_id == bot.uid:
        await event.delete()
        await tgbot.send_message(event.chat_id,
                                 ROZPIO4,
                                 buttons=[
                                     [Button.inline(
                                         "پێشوو ⫸ ", data="rozpio3"),
                                      Button.inline(
                                         "║ دەرچوون🕷️ ║ ⁦⁩", data="rozzag"),
                                      Button.inline(
                                         "⫷ دواتر", data="rozpio5")]
                                 ])
    else:
        await event.answer("تۆ ناتوانیت بۆت بەکاربهێنیت🌿. @xv7amo", alert=True)


@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"rozpio5"))) 
async def settings(event):#    بـەشـی بـایـۆ 5
    if event.sender_id == bot.uid:
        await event.delete()
        await tgbot.send_message(event.chat_id,
                                 ROZPIO5,
                                 buttons=[
                                     [Button.inline(
                                         "پێشوو ⫸ ", data="rozpio4"),
                                      Button.inline(
                                         "║ دەرچوون🕷️ ║⁦⁩", data="rozzag"),
                                      Button.inline(
                                         "⫷ دواتر", data="rozpio1")]
                                 ])
    else:
        await event.answer(" تۆ ناتوانیت بۆت بەکاربهێنیت🌿. @xv7amo", alert=True)

@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"rozmonth")))  
async def settings(event): #    بـەشـی لە دایـکـبـوون و مـانگـەکـان
    if event.sender_id == bot.uid:
        await event.delete()
        await tgbot.send_message(event.chat_id,
                                 "**⌯︙یەکێك لەمانەی خوارەوە هەڵبژێرە🌿💓.  **",
                                 buttons=[
                                     [Button.inline(
                                         "لەدایكبوون َِ🛹🖤", data="rozyear"),
                                      Button.inline(
                                         "مانگەکان َِ🛹🖤", data="months")],
                                     [Button.inline(
                                         "║ گەڕانەوە🕷️ ║", data="rozzag")]
                                 ])
    else:
        await event.answer("تۆ ناتوانیت بۆت بەکاربهێنیت @xv7amo", alert=True)


@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"months")))  
async def settings(event):#   بەشی مانگەکان🍀🤍.
    if event.sender_id == bot.uid:
        await event.delete()
        await tgbot.send_message(event.chat_id, 
                                 JMTHSH, 
                                 buttons=[[Button.inline("║ گەڕانەوە🕷️ ║", data="rozzag")]
                                 ])
    else:
        await event.answer("تۆ ناتوانیت ئەم بۆتە بەکاربهێنیت🌿.", alert=True)

@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"rozyear")))  
async def settings(event):#    بەشی ساڵەکان🤍.  :)
    if event.sender_id == bot.uid:
        await event.delete()
        await tgbot.send_message(event.chat_id, 
                                 YEAR, 
                                 buttons=[[Button.inline("║ گەڕانەوە🕷️ ║", data="rozmonth")]
                                 ])
    else:
        await event.answer("تۆ ناتوانیت ئەم بۆتە بەکاربهێنیت🌿.", alert=True)


@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"chanlan")))  
async def settings(event):  # # تـەواو بـوو :) ئەگەر تێکچوویت، ماندووبوونی ئەوانی ترت لەبیر بێت :) 🕷️🖤
    if event.sender_id == bot.uid:
        await event.delete()
        await tgbot.send_message(event.chat_id, 
                                 CHANLAN, 
                                 buttons=[[Button.inline("║ 🕷️گەڕانەوە ║", data="rozzag")]
                                 ])
    else:
        await event.answer("تۆ ناتوانیت ئەم بۆتە بەکاربهێنیت🌿.", alert=True)
