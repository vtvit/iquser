#    Credts @VTVIT
from geopy.geocoders import Nominatim
from telethon.tl import types

from iquser import iqub

from ..core.managers import edit_or_reply
from ..helpers import reply_id

plugin_category = "ئامێرەکان"


@iqub.iq_cmd(
    pattern="شوێن([\s\S]*)",
    command=("شوێن", plugin_category),
    info={
        "header": بۆ داواکردنی شوێنی مەبەست لەسەر ماپ",
        "بەکارهێنان": "{tr}شوێن + ناوچە/شار",
        "نموونە": "{tr}شوێن هەولێر",
    },
)
async def gps(event):
    "بۆ داواکردنی شوێنی مەبەست لەسەر ماپ"
    reply_to_id = await reply_id(event)
    input_str = event.pattern_match.group(1)
    catevent = await edit_or_reply(event, "**بارکردن**")
    geolocator = Nominatim(user_agent="catuserbot")
    if geoloc := geolocator.geocode(input_str):
        lon = geoloc.longitude
        lat = geoloc.latitude
        await event.client.send_file(
            event.chat_id,
            file=types.InputMediaGeoPoint(types.InputGeoPoint(lat, lon)),
            caption=f"**- شوێن : **`{input_str}`",
            reply_to=reply_to_id,
        )
        await catevent.delete()
    else:
        await catevent.edit("**- ببوورە .. نەمتوانی ئەم شوێنەم دەستبکەوێت دووبارە بگەڕێ  ...**")
