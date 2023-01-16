import asyncio

from iquser import iqub
from iquser.core.logger import logging

from ..Config import Config
from ..core.managers import edit_delete
from ..helpers.tools import media_type
from ..helpers.utils import _format
from ..sql_helper import no_log_pms_sql
from ..sql_helper.globals import addgvar, gvarstatus
from . import BOTLOG, BOTLOG_CHATID

LOGS = logging.getLogger(__name__)

plugin_category = "utils"


class LOG_CHATS:
    def __init__(self):
        self.RECENT_USER = None
        self.NEWPM = None
        self.COUNT = 0


LOG_CHATS_ = LOG_CHATS()


@iqub.iq_cmd(incoming=True, func=lambda e: e.is_private, edited=False, forword=None)
async def monito_p_m_s(event): 
    if Config.PM_LOGGER_GROUP_ID == -100:
        return
    if gvarstatus("PMLOG") and gvarstatus("PMLOG") == "false":
        return
    sender = await event.get_sender()
    if not sender.bot:
        chat = await event.get_chat()
        if not no_log_pms_sql.is_approved(chat.id) and chat.id != 777000:
            if LOG_CHATS_.RECENT_USER != chat.id:
                LOG_CHATS_.RECENT_USER = chat.id
                if LOG_CHATS_.NEWPM:
                    if LOG_CHATS_.COUNT > 1:
                        await LOG_CHATS_.NEWPM.edit(
                            LOG_CHATS_.NEWPM.text.replace(
                                "نامەیەکی نوێ ", f"{LOG_CHATS_.COUNT} "
                            )
                        )
                    else:
                        await LOG_CHATS_.NEWPM.edit(
                            LOG_CHATS_.NEWPM.text.replace(
                                "نامەیەکی نوێ ", f"{LOG_CHATS_.COUNT} "
                            )
                        )
                    LOG_CHATS_.COUNT = 0
                LOG_CHATS_.NEWPM = await event.client.send_message(
                    Config.PM_LOGGER_GROUP_ID,
                    f"👤{_format.mentionuser(sender.first_name , sender.id)}\n **نامەیەکی نوێی ناردووە** \nناوی بەکارهێنەر : `{chat.id}`",
                )
            try:
                if event.message:
                    await event.client.forward_messages(
                        Config.PM_LOGGER_GROUP_ID, event.message, silent=True
                    )
                LOG_CHATS_.COUNT += 1
            except Exception as e:
                LOGS.warn(str(e))
                
@iqub.iq_cmd(
    سەیڤ تایبەت (چالاک|ناچالاک)$",
    command=("سەیڤ تایبەت", plugin_category),
    info={
        "header": "To turn on or turn off logging of Private messages in pmlogger group.",
        "description": "Set PM_LOGGER_GROUP_ID in vars to work this",
        "usage": [
            "{tr}سەیڤ تایبەت چالاک",
            "{tr}سەیڤ تایبەت ناچالاک",
        ],
    },
)
async def set_pmlog(event):
    "بۆ چالاککردن و ناچالاککردنی سەیڤکردنی نامەکانی تایبەت"
    input_str = event.pattern_match.group(1)
    if input_str == "ناچالاک":
        h_type = False
    elif input_str == "چالاک":
        h_type = True
    if gvarstatus("PMLOG") and gvarstatus("PMLOG") == "false":
        PMLOG = False
    else:
        PMLOG = True
    if PMLOG:
        if h_type:
            await event.edit("**⌯︙ سەیڤکردنی نامەکانی تایبەت ئێستا گونجاوە ✅**")
        else:
            addgvar("PMLOG", h_type)
            await event.edit("**⌯︙ سەیڤکردنی نامەکانی تایبەت بە سەرکەوتوویی ناچالاککرا ✅**")
    elif h_type:
        addgvar("PMLOG", h_type)
        await event.edit("**⌯︙ سەیڤکردنی نامەکانی تایبەت بە سەرکەوتوویی چالاککرا ✅**")
    else:
        await event.edit("**⌯︙ سەیڤکردنی نامەی تایبەت ناچالاککراوە ✅**")


@iqub.iq_cmd(
    pattern="سەیڤ گرووپ (چالاک|ناچالاک)$",
    command=("سەیڤ گرووپ", plugin_category),
    info={
        "header": "To turn on or turn off group tags logging in pmlogger group.",
        "description": "Set PM_LOGGER_GROUP_ID in vars to work this",
        "usage": [
            "{tr}grplog on",
            "{tr}grplog off",
        ],
    },
)
async def set_grplog(event):
    "بۆ چالاککردن و ناچالاکردنی سەیڤکردنی نامەکانی گرووپەکان"
    input_str = event.pattern_match.group(1)
    if input_str == "ناچالاک":
        h_type = False
    elif input_str == "چالاک":
        h_type = True
    if gvarstatus("GRPLOG") and gvarstatus("GRPLOG") == "false":
        GRPLOG = False
    else:
        GRPLOG = True
    if GRPLOG:
        if h_type:
            await event.edit("**⌯︙ سەیڤکردنی نامەکانی گرووپەکان ئێستا گونجاوە ✅**")
        else:
            addgvar("GRPLOG", h_type)
            await event.edit("**⌯︙ سەیڤکردنی نامەکانی گرووپەکان بەسەرکەوتوویی ناچالاککرا ✅**")
    elif h_type:
        addgvar("GRPLOG", h_type)
        await event.edit("**⌯︙ سەیڤکردنی نامەی گرووپەکان بەسەرکەوتوویی چالاککرا ✅**")
    else:
        await event.edit("**⌯︙ سەیڤکردنی نامەکانی گرووپ ناچالاککراوە ✅**")
