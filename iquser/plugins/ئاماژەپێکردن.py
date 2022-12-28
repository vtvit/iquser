# By Reda for iquser
# Tel: @vtvit
#  :*
from iquser import iqub
import asyncio
from ..core.managers import edit_or_reply
from telethon.tl.types import ChannelParticipantAdmin
from telethon.tl.types import ChannelParticipantCreator
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.errors import UserNotParticipantError

spam_chats = []

@iqub.ar_cmd(pattern="تاگ(?:\s|$)([\s\S]*)")
async def menall(event):
    chat_id = event.chat_id
    if event.is_private:
        return await edit_or_reply(event, "** ᯽︙ ئەم فەرمانە تەنھا بۆ کەناڵ و گروپەکان بەکاردێت !**")
    msg = event.pattern_match.group(1)
    if not msg:
        return await edit_or_reply(event, "** ᯽︙ (تاگ)نامەیەك دابنێ بۆ ئاماژەپێکردن **")
    is_admin = False
    try:
        partici_ = await jepiq(GetParticipantRequest(
          event.chat_id,
          event.sender_id
        ))
    except UserNotParticipantError:
        is_admin = False
    spam_chats.append(chat_id)
    usrnum = 0
    usrtxt = ''
    async for usr in iqub.iter_participants(chat_id):
        if not chat_id in spam_chats:
            break
        usrtxt = f"{msg}\n[{usr.first_name}](tg://user?id={usr.id}) "
        await iqub.send_message(chat_id, usrtxt)
        await asyncio.sleep(2)
        await event.delete()
    try:
        spam_chats.remove(chat_id)
    except:
        pass
@jepiq.ar_cmd(pattern="لادانی تاگ")
async def ca_sp(event):
  if not event.chat_id in spam_chats:
    return await edit_or_reply(event, "** ᯽︙ 🤷🏻 هیچ تاگێك نییە بۆ لابردنی**")
  else:
    try:
      spam_chats.remove(event.chat_id)
    except:
      pass
    return await edit_or_reply(event, "** ᯽︙ بە سەرکەوتوویی ئاماژەپێکردن کۆتایی هات  ✓**")
