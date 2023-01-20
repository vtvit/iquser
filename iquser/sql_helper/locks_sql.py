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

jpvois1 = "jepthon/helpers/styles/Voic/ئۆنی چان.ogg"
jpvois2 = "jepthon/helpers/styles/Voic/ئۆنی چان2.ogg"
jpvois3 = "jepthon/helpers/styles/Voic/ئێھ.ogg"
jpvois4 = "jepthon/helpers/styles/Voic/ئەتاك.ogg"
jpvois5 = "jepthon/helpers/styles/Voic/ئەوە...ogg"
jpvois6 = "jepthon/helpers/styles/Voic/برادەر.ogg"
jpvois7 = "jepthon/helpers/styles/Voic/بمدەرێ.ogg"
jpvois8 = "jepthon/helpers/styles/Voic/سپایدەرمان.ogg"
jpvois9 = "jepthon/helpers/styles/Voic/سڵاو😂.ogg"
jpvois10 = "jepthon/helpers/styles/Voic/عەرەبی.ogg"
jpvois11 = "jepthon/helpers/styles/Voic/الكعدة وياكم حلوة.ogg"
jpvois12 = "jepthon/helpers/styles/Voic/الكمر اني النجم اني.ogg"
jpvois13 = "jepthon/helpers/styles/Voic/اللهم لا شماتة.ogg"
jpvois14 = "jepthon/helpers/styles/Voic/انا ما اكدر بعد.ogg"
jpvois15 = "jepthon/helpers/styles/Voic/بقولك اي يا قلبي كسمك.ogg"
jpvois16 = "jepthon/helpers/styles/Voic/تف على شرفك.ogg"
jpvois17 = "jepthon/helpers/styles/Voic/شجلبت.ogg"
jpvois18 = "jepthon/helpers/styles/Voic/شكد شفت ناس مدودة.ogg"
jpvois19 = "jepthon/helpers/styles/Voic/صباح القنادر.ogg"
jpvois20 = "jepthon/helpers/styles/Voic/ضحكة فيطية.ogg"
jpvois21 = "jepthon/helpers/styles/Voic/طار القلب.ogg"
jpvois22 = "jepthon/helpers/styles/Voic/غطيلي واغطيلك.ogg"
jpvois23 = "jepthon/helpers/styles/Voic/في منتصف الجبهة.ogg"
jpvois24 = "jepthon/helpers/styles/Voic/لا تقتل المتعة .ogg"
jpvois25 = "jepthon/helpers/styles/Voic/لا لتغلط.ogg"
jpvois26 = "jepthon/helpers/styles/Voic/لا يمه لا محاجي.ogg"


def get_locks(chat_id):
    try:
        return SESSION.query(Locks).get(str(chat_id))
    finally:
        SESSION.close()
