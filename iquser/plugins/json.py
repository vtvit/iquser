from iquser import iqub

from ..core.managers import edit_or_reply
from ..helpers.utils import _format

plugin_category = "ئامێرەکان"

# yaml_format is ported from uniborg
@iqub.zed_cmd(
    pattern="json$",
    command=("json", plugin_category),
    info={
        "header": "بۆ بەدەستهێنانی وردەکارییەکانی ئەو نامەیە بە فۆرماتی جاسۆن.",
        "بەکارهێنان": "{tr}json بە وەڵامدانەوەی نامەکە",
    },
)
async def _(event):
    "To get details of that message in json format."
    iqevent = await event.get_reply_message() if event.reply_to_msg_id else event
    the_real_message = iqevent.stringify()
    await edit_or_reply(event, the_real_message, parse_mode=_format.parse_pre)


@iqub.zed_cmd(
    pattern="yaml$",
    command=("yaml", plugin_category),
    info={
        "header": "بۆ بەدەستهێنانی وردەکارییەکانی ئەو نامەیە بە فۆرماتی yaml.",
        "بەکارهێنان": "{tr}yaml بە وەڵامدانەوەی نامەکە",
    },
)
async def _(event):
    "To get details of that message in yaml format."
    iqevent = await event.get_reply_message() if event.reply_to_msg_id else event
    the_real_message = _format.yaml_format(iqevent)
    await edit_or_reply(event, the_real_message, parse_mode=_format.parse_pre)
