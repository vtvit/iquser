import importlib
import sys
from pathlib import Path

from iquser import CMD_HELP, LOAD_PLUG

from ..Config import Config
from ..core import LOADED_CMDS, PLG_INFO
from ..core.logger import logging
from ..core.managers import edit_delete, edit_or_reply
from ..core.session import iqub
from ..helpers.tools import media_type
from ..helpers.utils import _iqtools, _iqutils, _format, install_pip, reply_id
from .decorators import admin_cmd, sudo_cmd

LOGS = logging.getLogger("iquser")


def load_module(shortname, plugin_path=None):
    if shortname.startswith("__"):
        pass
    elif shortname.endswith("_"):
        path = Path(f"jepthon/plugins/{shortname}.py")
        checkplugins(path)
        name = "iquser.plugins.{}".format(shortname)
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        LOGS.info("᯽︙بە سەرکەوتوویی فایلەکە دابەزا" + shortname)
    else:
        if plugin_path is None:
            path = Path(f"iquser/plugins/{shortname}.py")
            name = f"iquser.plugins.{shortname}"
        else:
            path = Path((f"{plugin_path}/{shortname}.py"))
            name = f"{plugin_path}/{shortname}".replace("/", ".")
        checkplugins(path)
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        mod.bot = iqub
        mod.LOGS = LOGS
        mod.Config = Config
        mod._format = _format
        mod.tgbot = iqub.tgbot
        mod.sudo_cmd = sudo_cmd
        mod.CMD_HELP = CMD_HELP
        mod.reply_id = reply_id
        mod.admin_cmd = admin_cmd
        mod._iqutils = _iqutils
        mod._iqtools = _iqtools
        mod.media_type = media_type
        mod.edit_delete = edit_delete
        mod.install_pip = install_pip
        mod.parse_pre = _format.parse_pre
        mod.edit_or_reply = edit_or_reply
        mod.logger = logging.getLogger(shortname)
        mod.borg = iqub
        spec.loader.exec_module(mod)
        # for imports
        sys.modules["iquser.plugins." + shortname] = mod
        LOGS.info("᯽︙بە سەرکەوتوویی فایل دابەزا ✓" + shortname)


def remove_plugin(shortname):
    try:
        cmd = []
        if shortname in PLG_INFO:
            cmd += PLG_INFO[shortname]
        else:
            cmd = [shortname]
        for cmdname in cmd:
            if cmdname in LOADED_CMDS:
                for i in LOADED_CMDS[cmdname]:
                    iqub.remove_event_handler(i)
                del LOADED_CMDS[cmdname]
        return True
    except Exception as e:
        LOGS.error(e)
    try:
        for i in LOAD_PLUG[shortname]:
            iqub.remove_event_handler(i)
        del LOAD_PLUG[shortname]
    except BaseException:
        pass
    try:
        name = f"iquser.plugins.{shortname}"
        for i in reversed(range(len(iqub._event_builders))):
            ev, cb = iqub._event_builders[i]
            if cb.__module__ == name:
                del iqub._event_builders[i]
    except BaseException:
        raise ValueError


def checkplugins(filename):
    with open(filename, "r") as f:
        filedata = f.read()
    filedata = filedata.replace("sendmessage", "send_message")
    filedata = filedata.replace("sendfile", "send_file")
    filedata = filedata.replace("editmessage", "edit_message")
    with open(filename, "w") as f:
        f.write(filedata)


# دەستپێکردنی فایلی یارمەتیدەری بۆت
def start_assistant(shortname):
    if shortname.startswith("__"):
        pass
    elif shortname.endswith("_"):
        import importlib
        import sys
        from pathlib import Path

        path = Path(f"iquser/plugins/assistant/{shortname}.py")
        name = "iquser.plugins.assistant.{}".format(shortname)
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        print("بۆتی یارمەتیدەر کاردەکات")
        print("بە سەرکەوتوویی دەستیپێکرد " + shortname)
    else:
        import importlib
        import sys
        from pathlib import Path

        path = Path(f"iquser/plugins/assistant/{shortname}.py")
        name = "iquser.plugins.assistant.{}".format(shortname)
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        mod.tgbot = bot.tgbot
        spec.loader.exec_module(mod)
        sys.modules["iquser.plugins.assistant" + shortname] = mod
        print("بەسەرکەوتوویی دابەزێنرا " + shortname)
