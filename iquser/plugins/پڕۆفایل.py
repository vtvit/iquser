import os

from telethon.errors.rpcerrorlist import UsernameOccupiedError
from telethon.tl import functions
from telethon.tl.functions.account import UpdateUsernameRequest
from telethon.tl.functions.channels import GetAdminedPublicChannelsRequest
from telethon.tl.functions.photos import DeletePhotosRequest, GetUserPhotosRequest
from telethon.tl.types import Channel, Chat, InputPhoto, User

from iquser import iqub

from ..Config import Config
from ..core.logger import logging
from ..core.managers import edit_delete, edit_or_reply

LOGS = logging.getLogger(__name__)
plugin_category = "utils"


# ====================== CONSTANT ===============================
INVALID_MEDIA = "᯽︙ ئەم وێنەیە نادروستە.```"
PP_CHANGED = "⌔︙**  بە سەرکەوتوویی وێنەی ئەکاونتت گۆڕا. ⌁،**"
PP_TOO_SMOL = "** ᯽︙ ئەو وێنەیە بچووکە تکایە دانەیەکی گونجاوتر دابنێ .⌁،**"
PP_ERROR = "** ᯽︙ هەڵەیەك ڕوویدا لەکاتی پرۆسەکردنی وێنەکە .  ⌁**"
BIO_SUCCESS = "** ᯽︙ بە سەرکەوتوویی بایۆی ئەکاونتت گۆڕا .⌁،**"
NAME_OK = "** ᯽︙ بە سەرکەوتوویی ناوی ئەکاونتت گۆڕا. ⌁**"
USERNAME_SUCCESS = "**᯽︙ بە سەرکەوتوویی ناوی بەکارهێنەر گۆڕا ⌁،**"
USERNAME_TAKEN = "**᯽︙  ئەوە ناوی بەکارهێنەرە ⌁ ،**"
# ===============================================================


@iqub.iq_cmd(
    pattern="بایۆ (.*)",
    command=("بایۆ", plugin_category),
    info={
        "سەری پەڕە": "بۆ دانانی بایۆ بۆ سەر ئەکاونت.",
        "بەکارهێنان": "{tr}بایۆ <بایۆکەت>",
    },
)
async def _(event):
    "To set bio for this account."
    bio = event.pattern_match.group(1)
    try:
        await event.client(functions.account.UpdateProfileRequest(about=bio))
        await edit_delete(event, "᯽︙ بە سەرکەوتوویی بایۆکەت گۆڕا ✅")
    except Exception as e:
        await edit_or_reply(event, f"**هەڵەیە:**\n`{str(e)}`")


@iqub.iq_cmd(
    pattern="ناو (.*)",
    command=("ناو", plugin_category),
    info={
        "سەری پەڕە": "بۆ دانانی یان گۆڕینی ناوی ئەکاونت.",
        "بەکارهێنان": ["{tr}ناو ناوی یەکەم ; ناوی دووەم", "{tr}ناو ناوی یەکەم"],
    },
)
async def _(event):
    "To set/change name for this account."
    names = event.pattern_match.group(1)
    first_name = names
    last_name = ""
    if ";" in names:
        first_name, last_name = names.split("|", 1)
    try:
        await event.client(
            functions.account.UpdateProfileRequest(
                first_name=first_name, last_name=last_name
            )
        )
        await edit_delete(event, "᯽︙ بە سەرکەوتوویی ناوەکەت گۆڕا ✅")
    except Exception as e:
        await edit_or_reply(event, f"**هەڵەیە:**\n`{str(e)}`")


@iqub.iq_cmd(
    pattern="وێنە$",
    command=("وێنە", plugin_category),
    info={
        "سەری پەڕە": "بۆ دانانی وێنە لە ئەکاونت",
        "بەکارهێنان": "{tr}وێنە <وەڵامدانەوەی وێنە یان گیف>",
    },
)
async def _(event):
    "To set profile pic for this account."
    reply_message = await event.get_reply_message()
    catevent = await edit_or_reply(
        event, "**...**"
    )
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    photo = None
    try:
        photo = await event.client.download_media(
            reply_message, Config.TMP_DOWNLOAD_DIRECTORY
        )
    except Exception as e:
        await catevent.edit(str(e))
    else:
        if photo:
            await catevent.edit("᯽︙ کـەمێـك چـاوەڕێ بـکە ")
            if photo.endswith((".mp4", ".MP4")):
                # https://t.me/tgbetachat/324694
                size = os.stat(photo).st_size
                if size > 2097152:
                    await catevent.edit("᯽︙ پێویستە قەبارەکەی 2 مێگا بێت ✅")
                    os.remove(photo)
                    return
                catpic = None
                catvideo = await event.client.upload_file(photo)
            else:
                catpic = await event.client.upload_file(photo)
                catvideo = None
            try:
                await event.client(
                    functions.photos.UploadProfilePhotoRequest(
                        file=catpic, video=catvideo, video_start_ts=0.01
                    )
                )
            except Exception as e:
                await catevent.edit(f"**هەڵەیە:**\n`{str(e)}`")
            else:
                await edit_or_reply(
                    catevent, "᯽︙ بە سەرکەوتوویی وێنەکەت گۆڕا ✅"
                )
    try:
        os.remove(photo)
    except Exception as e:
        LOGS.info(str(e))


@iqub.iq_cmd(
    pattern="ناوی بەکارهێنەر (.*)",
    command=("ناوی بەکارهێنەر", plugin_category),
    info={
        "سەری پەڕە": "بۆ دانانی ناوی بەکارهێنەر یان نوێ کردنەوەی.",
        "بەکارهێنان": "{tr}ناوی بەکارهێنەر <ناوی بەکارهێنەری نوێ>",
    },
)
async def update_username(username):
    """For .username command, set a new username in Telegram."""
    newusername = username.pattern_match.group(1)
    try:
        await username.client(UpdateUsernameRequest(newusername))
        await edit_delete(event, USERNAME_SUCCESS)
    except UsernameOccupiedError:
        await edit_or_reply(event, USERNAME_TAKEN)
    except Exception as e:
        await edit_or_reply(event, f"**هەڵەیە:**\n`{str(e)}`")


@jepiq.ar_cmd(
    pattern="ئەکاونتم$",
    command=("ئەکاونتم", plugin_category),
    info={
        "سەری پەڕە": "بۆ هێنانی چالاکیەکانی ئەکاونت.",
        "بەکارهێنان": "{tr}ئەکاونتم",
    },
)
async def count(event):
    """For .count command, get profile stats."""
    u = 0
    g = 0
    c = 0
    bc = 0
    b = 0
    result = ""
    catevent = await edit_or_reply(event, "᯽︙ کەمێك چاوەڕێ بکە .. ")
    dialogs = await event.client.get_dialogs(limit=None, ignore_migrated=True)
    for d in dialogs:
        currrent_entity = d.entity
        if isinstance(currrent_entity, User):
            if currrent_entity.bot:
                b += 1
            else:
                u += 1
        elif isinstance(currrent_entity, Chat):
            g += 1
        elif isinstance(currrent_entity, Channel):
            if currrent_entity.broadcast:
                bc += 1
            else:
                c += 1
        else:
            LOGS.info(d)

    result += f"**᯽︙ بەکارهێنەران:**\t**{u}**\n"
    result += f"**᯽︙ گرووپەکان:**\t**{g}**\n"
    result += f"**᯽︙  گرووپە نایابەکان:**\t**{c}**\n"
    result += f"**᯽︙ چەناڵەکان:**\t**{bc}**\n"
    result += f"**᯽︙ بۆتەکان:**\t**{b}**"

    await catevent.edit(result)


@iqub.iq_cmd(
    pattern="سڕینەوەی وێنە ?(.*)",
    command=("سڕینەوەی وێنە", plugin_category),
    info={
        "header": "To delete profile pic for this account.",
        "description": "If you havent mentioned no of profile pics then only 1 will be deleted.",
        "usage": ["{tr}سڕینەوەی وێنە <هیچ وێنەیەك نیە بۆ سڕینەوە>", "{tr}سڕینەوەی وێنە"],
    },
)
async def remove_profilepic(delpfp):
    """For .delpfp command, delete your current profile picture in Telegram."""
    group = delpfp.text[8:]
    if group == "all":
        lim = 0
    elif group.isdigit():
        lim = int(group)
    else:
        lim = 1
    pfplist = await delpfp.client(
        GetUserPhotosRequest(user_id=delpfp.sender_id, offset=0, max_id=0, limit=lim)
    )
    input_photos = [
        InputPhoto(
            id=sep.id,
            access_hash=sep.access_hash,
            file_reference=sep.file_reference,
        )
        for sep in pfplist.photos
    ]
    await delpfp.client(DeletePhotosRequest(id=input_photos))
    await edit_delete(
        delpfp, f"᯽︙ سڕایەوە {len(input_photos)} وێنەی ئەکاونتت بە سەرکەوتوویی ✅"
    )


@iqub.iq_cmd(
    pattern="پێکهاتە$",
    command=("پێکهاتە", plugin_category),
    info={
        "header": "To list public channels or groups created by this account.",
        "usage": "{tr}myusernames",
    },
)
async def _(event):
    "To list all public channels and groups."
    result = await event.client(GetAdminedPublicChannelsRequest())
    output_str = "᯽︙ هەموو گرووپ و چەناڵەکانی کە تۆ دروستت کردووە🖤 :\n"
    output_str += "".join(
        f" - {channel_obj.title} @{channel_obj.username} \n"
        for channel_obj in result.chats
    )
    await edit_or_reply(event, output_str)

#فایلی پڕۆفایلی تایبەت بە VTVIT
