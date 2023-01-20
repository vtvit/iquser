from sqlalchemy import Boolean, Column, String

from . import BASE, SESSION

class Locks(BASE):
    __tablename__ = "locks"
    chat_id = Column(String(14), primary_key=True)
    # Booleans are for "is this locked", _NOT_ "is this allowed"
    bots = Column(Boolean, default=False)
    commands = Column(Boolean, default=False)
    email = Column(Boolean, default=False)
    forward = Column(Boolean, default=False)
    url = Column(Boolean, default=False)

    def __init__(self, chat_id):
        self.chat_id = str(chat_id)  # ensure string
        self.bots = False
        self.commands = False
        self.email = False
        self.forward = False
        self.url = False


Locks.__table__.create(checkfirst=True)


def init_locks(chat_id, reset=False):
    curr_restr = SESSION.query(Locks).get(str(chat_id))
    if reset:
        SESSION.delete(curr_restr)
        SESSION.flush()
    restr = Locks(str(chat_id))
    SESSION.add(restr)
    SESSION.commit()
    return restr


def update_lock(chat_id, lock_type, locked):
    curr_perm = SESSION.query(Locks).get(str(chat_id))
    if not curr_perm:
        curr_perm = init_locks(chat_id)
    if lock_type == "bots":
        curr_perm.bots = locked
    elif lock_type == "commands":
        curr_perm.commands = locked
    elif lock_type == "email":
        curr_perm.email = locked
    elif lock_type == "forward":
        curr_perm.forward = locked
    elif lock_type == "url":
        curr_perm.url = locked
    SESSION.add(curr_perm)
    SESSION.commit()


def is_locked(chat_id, lock_type):
    curr_perm = SESSION.query(Locks).get(str(chat_id))
    SESSION.close()
    if not curr_perm:
        return False
    if lock_type == "bots":
        return curr_perm.bots
    if lock_type == "commands":
        return curr_perm.commands
    if lock_type == "email":
        return curr_perm.email
    if lock_type == "forward":
        return curr_perm.forward
    if lock_type == "url":
        return curr_perm.url

iqvois1 = "jepthon/helpers/styles/Voic/ئۆنی چان.ogg"
iqvois2 = "jepthon/helpers/styles/Voic/ئۆنی چان2.ogg"
iqvois3 = "jepthon/helpers/styles/Voic/ئێھ.ogg"
iqvois4 = "jepthon/helpers/styles/Voic/ئەتاك.ogg"
iqvois5 = "jepthon/helpers/styles/Voic/ئەوە...ogg"
iqvois6 = "jepthon/helpers/styles/Voic/برادەر.ogg"
iqvois7 = "jepthon/helpers/styles/Voic/بمدەرێ.ogg"
iqvois8 = "jepthon/helpers/styles/Voic/سپایدەرمان.ogg"
iqvois9 = "jepthon/helpers/styles/Voic/سڵاو😂.ogg"
iqvois10 = "jepthon/helpers/styles/Voic/عەرەبی.ogg"
iqvois11 = "jepthon/helpers/styles/Voic/سویی.ogg"
iqvois12 = "jepthon/helpers/styles/Voic/کەلاری.ogg"
iqvois13 = "jepthon/helpers/styles/Voic/یا مرحبا.ogg"
 
def get_locks(chat_id):
    try:
        return SESSION.query(Locks).get(str(chat_id))
    finally:
        SESSION.close()
