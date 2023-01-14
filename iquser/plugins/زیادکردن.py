from jepthon import *
from jepthon import jepiq
from jepthon.utils import admin_cmd
from telethon.tl.types import Channel, Chat, User
from telethon.tl import functions, types
from telethon.tl.functions.messages import  CheckChatInviteRequest, GetFullChatRequest
from telethon.errors import (ChannelInvalidError, ChannelPrivateError, ChannelPublicGroupNaError, InviteHashEmptyError, InviteHashExpiredError, InviteHashInvalidError)
from telethon.tl.functions.channels import GetFullChannelRequest, GetParticipantsRequest



async def get_chatinfo(event):
    chat = event.pattern_match.group(1)
    chat_info = None
    if chat:
        try:
            chat = int(chat)
        except ValueError:
            pass
    if not chat:
        if event.reply_to_msg_id:
            replied_msg = await event.get_reply_message()
            if replied_msg.fwd_from and replied_msg.fwd_from.channel_id is not None:
                chat = replied_msg.fwd_from.channel_id
        else:
            chat = event.chat_id
    try:
        chat_info = await event.client(GetFullChatRequest(chat))
    except:
        try:
            chat_info = await event.client(GetFullChannelRequest(chat))
        except ChannelInvalidError:
            await event.reply("**▾∮ گرووپ یان چەناڵ نەدۆزرایەوە **")
            return None
        except ChannelPrivateError:
            await event.reply("**▾∮  ناتوانم  فەرمانەکە بەکاربێنم لە گرووپەکان یان چەناڵە تایبەتەکانەوە**")
            return None
        except ChannelPublicGroupNaError:
            await event.reply("**▾∮ گرووپ یان چەناڵ نەدۆزرایەوە**")
            return None
        except (TypeError, ValueError) as err:
            await event.reply("**▾∮ بەستەری گرووپ درووست نییە**")
            return None
    return chat_info


def make_mention(user):
    if user.username:
        return f"@{user.username}"
    else:
        return inline_mention(user)


def inline_mention(user):
    full_name = user_full_name(user) or "No Name"
    return f"[{full_name}](tg://user?id={user.id})"


def user_full_name(user):
    names = [user.first_name, user.last_name]
    names = [i for i in list(names) if i]
    full_name = ' '.join(names)
    return full_name
 


# نوسینگەی بۆتی زیرەك
#  اخـخـخ


@iqub.on(admin_cmd(pattern=r"زیادکردن ?(.*)"))
async def get_users(event):   
    sender = await event.get_sender() ; me = await event.client.get_me()
    if not sender.id == me.id:
        roz = await event.reply("**▾∮ پرۆسەکە ئەنجام دەدرێت کەمێك چاوەڕێ بکە 🧸♥ ...**")
    else:
        roz = await event.edit("**▾∮ پرۆسەکە ئەنجام دەدرێت کەمێك چاوەڕێ بکە 🧸♥ ...**.")
    iquser = await get_chatinfo(event) ; chat = await event.get_chat()
    if event.is_private:
              return await roz.edit("**▾∮ ناتوانم بەکارهێنەرانی ئێرە زیاد بکەم**")    
    s = 0 ; f = 0 ; error = 'None'   
  
    await roz.edit("**▾∮ دۆخی زیادکردن:**\n\n**▾∮ زانیاری بەکارهێنەر کۆکراوەتەوە 🔄 ...⏣**")
    async for user in event.client.iter_participants(JepThon.full_chat.id):
                try:
                    if error.startswith("Too"):
                        return await roz.edit(f"**دۆخی زیادکردنەکە بە هەڵەکان کۆتایی هات**\n- (**لەوانەیە فشارێك لەسەر فەرمانەکە هەبێت، هەوڵ بدە دواتر بیدۆزیتەوە 🧸**) \n**هەڵەیە** : \n`{error}`\n\n• زیادکردن `{s}` \n• هەڵە لە زیادکردن  `{f}`"),
                    await event.client(functions.channels.InviteToChannelRequest(channel=chat,users=[user.id]))
                    s = s + 1                                                    
                    await roz.edit(f"**▾∮ زیادکرا 🧸♥**\n\n• زیادبکە `{s}` \n•  هەڵە لە زیادکردن  `{f}` \n\n**× کۆتا هەڵە:** `{error}`") 
                except Exception as e:
                    error = str(e) ; f = f + 1             
    return await roz.edit(f"**▾∮زیادکردن تەواوبوو ✅** \n\n•  بە سەرکەوتوویی زیادکرا `{s}` \n• هەڵە لە زیادکردن  `{f}`")
