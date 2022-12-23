import asyncio
import datetime
import inspect
import re
import sys
import traceback
from pathlib import Path
from typing import Dict, List, Union

from telethon import TelegramClient, events
from telethon.errors import (
    AlreadyInConversationError,
    BotInlineDisabledError,
    BotResponseTimeoutError,
    ChatSendInlineForbiddenError,
    ChatSendMediaForbiddenError,
    ChatSendStickersForbiddenError,
    FloodWaitError,
    MessageIdInvalidError,
    MessageNotModifiedError,
)

from ..Config import Config
from ..helpers.utils.events import checking
from ..helpers.utils.format import paste_message
from ..helpers.utils.utils import runcmd
from ..sql_helper.globals import gvarstatus
from . import BOT_INFO, CMD_INFO, GRP_INFO, LOADED_CMDS, PLG_INFO
from .cmdinfo import _format_about
from .data import _sudousers_list, blacklist_chats_list, sudo_enabled_cmds
from .events import *
from .fasttelethon import download_file, upload_file
from .logger import logging
from .managers import edit_delete
from .pluginManager import get_message_link, restart_script

LOGS = logging.getLogger(__name__)


class REGEX:
    def __init__(self):
        self.regex = ""
        self.regex1 = ""
        self.regex2 = ""


REGEX_ = REGEX()
sudo_enabledcmds = sudo_enabled_cmds()


class IQUserBotClient(TelegramClient):
    def iq_cmd(
        self: TelegramClient,
        pattern: str or tuple = None,
        info: Union[str, Dict[str, Union[str, List[str], Dict[str, str]]]]
        or tuple = None,
        groups_only: bool = False,
        private_only: bool = False,
        allow_sudo: bool = True,
        edited: bool = True,
        forword=False,
        disable_errors: bool = False,
        command: str or tuple = None,
        **kwargs,
    ) -> callable:  # sourcery no-metrics
        kwargs["func"] = kwargs.get("func", lambda e: e.via_bot_id is None)
        kwargs.setdefault("forwards", forword)
        if gvarstatus("blacklist_chats") is not None:
            kwargs["blacklist_chats"] = True
            kwargs["chats"] = blacklist_chats_list()
        stack = inspect.stack()
        previous_stack_frame = stack[1]
        file_test = Path(previous_stack_frame.filename)
        file_test = file_test.stem.replace(".py", "")
        if command is not None:
            command = list(command)
            if not command[1] in BOT_INFO:
                BOT_INFO.append(command[1])
            try:
                if file_test not in GRP_INFO[command[1]]:
                    GRP_INFO[command[1]].append(file_test)
            except BaseException:
                GRP_INFO.update({command[1]: [file_test]})
            try:
                if command[0] not in PLG_INFO[file_test]:
                    PLG_INFO[file_test].append(command[0])
            except BaseException:
                PLG_INFO.update({file_test: [command[0]]})
            if not command[0] in CMD_INFO:
                CMD_INFO[command[0]] = [_format_about(info)]
        if pattern is not None:
            if (
                pattern.startswith(r"\#")
                or not pattern.startswith(r"\#")
                and pattern.startswith(r"^")
            ):
                REGEX_.regex1 = REGEX_.regex2 = re.compile(pattern)
            else:
                reg1 = "\\" + Config.COMMAND_HAND_LER
                reg2 = "\\" + Config.SUDO_COMMAND_HAND_LER
                REGEX_.regex1 = re.compile(reg1 + pattern)
                REGEX_.regex2 = re.compile(reg2 + pattern)

        def decorator(func):  # sourcery no-metrics
            async def wrapper(check):  # sourcery no-metrics
                if groups_only and not check.is_group:
                    return await edit_delete(
                        check, "**⪼ ببوورە، بەکارهێنانی ئەم فەرمانە تەنھا لە گرووپدایە.  𓆰،**", 10
                    )
                if private_only and not check.is_private:
                    return await edit_delete(
                        check, "**⪼ ئەم بەکارھێنانی ئەم فەرمانە تەنھا لە چاتی تایبەتدایە  𓆰،**", 10
                    )
                try:
                    await func(check)
                except events.StopPropagation as e:
                    raise events.StopPropagation from e
                except KeyboardInterrupt:
                    pass
                except MessageNotModifiedError:
                    LOGS.error("نامەکە هاوشێوەی نامەی پێشوو بوو")
                except MessageIdInvalidError:
                    LOGS.error("نامە سڕاوەتەوە یان نەدۆزرایەوە")
                except BotInlineDisabledError:
                    await edit_delete(check, "**⌔∮ پێویستە سەرەتا دۆخی ئۆنلاین چالاک بکەیت)
                except ChatSendStickersForbiddenError:
                    await edit_delete(
                        check, "**- 10 ,"** ئەم گرووپە ڕێگە بە ناردنی ستەیکەر نادات بۆ ئێرە
                    )
                except BotResponseTimeoutError:
                    await edit_delete(
                        check, "⪼ ئەم تایبەتمەندیە بەکاربھێنە پاش ماوەیەکی کەم ناتوانیت ئێستا وەڵام بدەیتەوە ", 10
                    )
                except ChatSendMediaForbiddenError:
                    await edit_delete(check, "**⪼ ئەم گرووپە ڕێگە بە ناردنی میدیا نادات بۆ ئێرە 𓆰،**", 10)
                except AlreadyInConversationError:
                    await edit_delete(
                        check,
                        "**- گفتووگۆکە هەر ئێستا لەگەڵ چاتێکی دیاریکراودا بەڕێوەدەچێت .. دووبارە هەوڵ بدەوە کەمێکی تر**",
                        10,
                    )
                except ChatSendInlineForbiddenError:
                    await edit_delete(
                        check, "**- ببوورە .. ئۆنلاین لەم گروپەدا داخراوە **", 10
                    )
                except FloodWaitError as e:
                    LOGS.error(
                        f"وەستانی کاتی بەهۆی دووبارەبوونەوە {e.seconds} ڕوداو. چاوەڕێکە {e.seconds} دووەم و دووبارە هەوڵ بدە"
                    )
                    await check.delete()
                    await asyncio.sleep(e.seconds + 5)
                except BaseException as e:
                    LOGS.exception(e)
                    if not disable_errors:
                        if Config.PRIVATE_GROUP_BOT_API_ID == 0:
                            return
                        date = (datetime.datetime.now()).strftime("%m/%d/%Y, %H:%M:%S")
                        ftext = f"\nدادەبەزێت تەنھا لێرە ،\
                                  \n\nنسجل فقـط تقريـر الإشعـار وتـاريخـه ،\
                                  \n\nئێمە ڕێز لە تایبەتمەندیەکەت دەگرین.\
                                  \n\nناردنی ئەم نامەیە تەنھا بۆ گەشەپێدەری سەرچاوەیە @VTVIT\
                                  \n\n--------دەستپێکردنی تۆماری بە دواکەوتنی بۆتی زیرەك 𝙄𝙌𝙐𝙎𝙀𝙍 メ--------\
                                  \n- بەروار : {date}\n- ناسنامەی گرووپ  : {str(check.chat_id)}\
                                  \n- ناسنامەی کەسەکە : {str(check.sender_id)}\
                                  \n- بەستەری نامەکە : {await check.client.get_msg_link(check)}\
                                  \n\n- ڕاپۆرت :\n{str(check.text)}\
                                  \n\n- وردەکاریەکان :\n{str(traceback.format_exc())}\
                                  \n\n- دەقی ئاگاداری :\n{str(sys.exc_info()[1])}"
                        new = {
                            "error": str(sys.exc_info()[1]),
                            "date": datetime.datetime.now(),
                        }
                        ftext += "\n\n--------کۆتا تۆماری بە دواکەوتنی بۆتی زیرەك 𝙄𝙌𝙐𝙎𝙀𝙍 メ--------"
                        ftext += "\n\n\n- دوا 5 فایل نوێکرایەوە :\n"
                        command = 'git log --pretty=format:"%an: %s" -5'
                        output = (await runcmd(command))[:2]
                        result = output[0] + output[1]
                        ftext += result
                        pastelink = await paste_message(
                            ftext, pastetype="s", markdown=False
                        )
                        link = "[𐇮 𝙑𝙏𝙑𝙄𝙏 𝞝 بۆتی زیرەك 𐇮](https://t.me/VTVIT)"
                        text = (
                            "**✘ ڕاپۆرتی ئاگاداری بۆتی زیرەك  𝙄𝙌 ✘**\n\n"
                            + "- دەتوانیت ڕاپۆرتی ئەم تێبینیە بدەیت .. "
                        )
                        text += f"- ناردنی ئەم نامەیە تەنھا بۆ گەشەپێدەری سەرچاوەیە{link}.\n\n"
                        text += (
                            "-بۆ ئاگادارکردنەوەی گەشەپێدەرەکە لە ئاگاداریەکە .. تا ئەو کاتەی ئاگاداری  دەکەیتەوە\n\n"
                        )
                        text += f"**- نامەی ئاگاداری :** [{new['error']}]({pastelink})"
                        await check.client.send_message(
                            Config.PRIVATE_GROUP_BOT_API_ID, text, link_preview=False
                        )

            from .session import iqub

            if not func.__doc__ is None:
                CMD_INFO[command[0]].append((func.__doc__).strip())
            if pattern is not None:
                if command is not None:
                    if command[0] in LOADED_CMDS and wrapper in LOADED_CMDS[command[0]]:
                        return None
                    try:
                        LOADED_CMDS[command[0]].append(wrapper)
                    except BaseException:
                        LOADED_CMDS.update({command[0]: [wrapper]})
                if edited:
                    iqub.add_event_handler(
                        wrapper,
                        MessageEdited(pattern=REGEX_.regex1, outgoing=True, **kwargs),
                    )
                iqub.add_event_handler(
                    wrapper,
                    NewMessage(pattern=REGEX_.regex1, outgoing=True, **kwargs),
                )
                if allow_sudo and gvarstatus("sudoenable") is not None:
                    if command is None or command[0] in sudo_enabledcmds:
                        if edited:
                            iqub.add_event_handler(
                                wrapper,
                                MessageEdited(
                                    pattern=REGEX_.regex2,
                                    from_users=_sudousers_list(),
                                    **kwargs,
                                ),
                            )
                        iqub.add_event_handler(
                            wrapper,
                            NewMessage(
                                pattern=REGEX_.regex2,
                                from_users=_sudousers_list(),
                                **kwargs,
                            ),
                        )
            else:
                if file_test in LOADED_CMDS and func in LOADED_CMDS[file_test]:
                    return None
                try:
                    LOADED_CMDS[file_test].append(func)
                except BaseException:
                    LOADED_CMDS.update({file_test: [func]})
                if edited:
                    iqub.add_event_handler(func, events.MessageEdited(**kwargs))
                iqub.add_event_handler(func, events.NewMessage(**kwargs))
            return wrapper

        return decorator

    def bot_cmd(
        self: TelegramClient,
        disable_errors: bool = False,
        edited: bool = False,
        forword=False,
        **kwargs,
    ) -> callable:  # sourcery no-metrics
        kwargs["func"] = kwargs.get("func", lambda e: e.via_bot_id is None)
        kwargs.setdefault("forwards", forword)

        def decorator(func):
            async def wrapper(check):
                try:
                    await func(check)
                except events.StopPropagation as e:
                    raise events.StopPropagation from e
                except KeyboardInterrupt:
                    pass
                except MessageNotModifiedError:
                    LOGS.error("Message was same as previous message")
                except MessageIdInvalidError:
                    LOGS.error("Message was deleted or cant be found")
                except BaseException as e:
                    # Check if we have to disable error logging.
                    LOGS.exception(e)  # Log the error in console
                    if not disable_errors:
                        if Config.PRIVATE_GROUP_BOT_API_ID == 0:
                            return
                        date = (datetime.datetime.now()).strftime("%m/%d/%Y, %H:%M:%S")
                        ftext = f"\nفایلەکە دادەبەزێت تەنھا لێرە ،\
                                  \n\nئێمە تەنھا ڕاپۆرتی ئاگاداریەکان و بەروارەکە تۆمار دەکەین ،\
                                  \n\nئێمە ڕێز لە تایبەتمەندیەکەت دەگرین.\
                                  \n\nناردنی ئەم نامەیە تەنھا بۆ گەشەپێدەری سەرچاوەیە @IQ7amo\
                                  \n\n--------دەستپێکردنی تۆماری بەدواکەوتنی بۆتی زیرەك 𝙄𝙌𝙐𝙎𝙀𝙍 メ--------\
                                  \n- بەروار : {date}\n- ناسنامەی گرووپ : {str(check.chat_id)}\
                                  \n- ناسنامەی کەسەکە : {str(check.sender_id)}\
                                  \n- بەستەری نامەکە : {await check.client.get_msg_link(check)}\
                                  \n\n- ڕاپۆرت :\n{str(check.text)}\
                                  \n\n- وردەکاریەکان :\n{str(traceback.format_exc())}\
                                  \n\n- دەقی ئاگاداری :\n{str(sys.exc_info()[1])}"
                        new = {
                            "error": str(sys.exc_info()[1]),
                            "date": datetime.datetime.now(),
                        }
                        ftext += "\n\n--------کۆتا تۆماری بەدواکەوتنی بۆتی زیرەك 𝙄𝙌𝙐𝙎𝙀𝙍 メ--------"
                        command = 'git log --pretty=format:"%an: %s" -5'
                        ftext += "\n\n\n- دوا 5 فایل نوێکرایەوە :\n"
                        output = (await runcmd(command))[:2]
                        result = output[0] + output[1]
                        ftext += result
                        pastelink = await paste_message(
                            ftext, pastetype="s", markdown=False
                        )
                        text = "**✘ ڕاپۆرتی ئاگاداری بۆتی زیرەك 𝙄𝙌 ✘**\n\n "
                        link = "[𐇮 𝙑𝙏𝙑𝙄𝙏 𝞝 بۆتی زیرەك 𐇮](https://t.me/IQUSER0)"
                        text += "- دەتوانیت راپۆرتی ئەم تێبینیە بدەیت .. "
                        text += f"- ناردنی ئەم نامەیە تەنھا بۆ گەشەپێدەری سەرچاوەیە {link}.\n"
                        text += (
                            "- بۆ ئاگادارکردنەوەی گەشەپێدەرەکە لە ئاگاداریەکە .. تا ئەو کاتەی ئاگاداری دەکەیتەوە\n\n"
                        )
                        text += f"**- نامەی ئاگاداری :** [{new['error']}]({pastelink})"
                        await check.client.send_message(
                            Config.PRIVATE_GROUP_BOT_API_ID, text, link_preview=False
                        )

            from .session import zedub

            if edited is True:
                iqubub.tgbot.add_event_handler(func, events.MessageEdited(**kwargs))
            else:
                iqub.tgbot.add_event_handler(func, events.NewMessage(**kwargs))

            return wrapper

        return decorator

    async def get_traceback(self, exc: Exception) -> str:
        return "".join(
            traceback.format_exception(etype=type(exc), value=exc, tb=exc.__traceback__)
        )

    def _kill_running_processes(self) -> None:
        """Kill all the running asyncio subprocessess"""
        for _, process in self.running_processes.items():
            try:
                process.kill()
                LOGS.debug("Killed %d which was still running.", process.pid)
            except Exception as e:
                LOGS.debug(e)
        self.running_processes.clear()


IQUserBotClient.fast_download_file = download_file
IQUserBotClient.fast_upload_file = upload_file
IQUserBotClient.reload = restart_script
IQUserBotClient.get_msg_link = get_message_link
IQUserBotClient.check_testcases = checking
try:
    send_message_check = TelegramClient.send_message
except AttributeError:
    IQUserBotClient.send_message = send_message
    IQUserBotClient.send_file = send_file
    IQUserBotClient.edit_message = edit_message
