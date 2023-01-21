import sys
import os
from typing import Any, Dict, List, Union
from glob import glob
from iquser import *
from iquser.helpers.functions.functions import translate
try:
    from yaml import safe_load
except ModuleNotFoundError:
    from iquser.helpers.functions.functions import safe_load

os.getenv("LANGUAGE", "kr")

languages = {}



for file in glob("vtvit/strings/*yml"):
    if file.endswith(".yml"):
        code = file.split("/")[-1].split("\\")[-1][:-4]
        try:
            languages[code] = safe_load(
                open(file, encoding="UTF-8"),
            )
        
        except Exception as er:
            LOGS.info(f"Error in {file[:-4]} language file")
            LOGS.exception(er)


def get_string(key: str, _res: bool = True) -> Any:
    lang = "kr"
    try:
        return languages[lang][key]
    except KeyError:
        try:
            ar_ = languages["ar"][key]
            tr = translate(ar_, lang_tgt=lang).replace("\ N", "\n")
            if en_.count("{}") != tr.count("{}"):
                tr = ar_
            if languages.get(lang):
                languages[lang][key] = tr
            else:
                languages.update({lang: {key: tr}})
            return tr
        except KeyError:
            if not _res:
                return
            return f"ئاگادارکردنەوە:هیچ زنجیرەیەك ناتوانرێت دابەزێت بە کلیلەکان  `{key}`"
        except TypeError:
            pass
        except Exception as er:
            LOGS.exception(er)
        if not _res:
            return None
        return languages["kr"].get(key) or f"بارکردنی زنجیرەی زمان شکستی هێنا '{key}'"

def get_help(key):
    doc = get_string(f"help_{key}", _res=False)
    if doc:
        return get_string("cmda") + doc

def get_languages() -> Dict[str, Union[str, List[str]]]:
    return {
        code: {
            "name": languages[code]["name"],
            "natively": languages[code]["natively"],
            "authors": languages[code]["authors"],
        }
        for code in languages
    }
