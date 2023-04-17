from __future__ import annotations
from django.contrib.sessions import SessionBase
from App.models import UserModel


class SessionUser:
    def __init__(self, uid: str):
        assert uid != "", "uid is empty"
        self.uid: str | None = uid

    def save(self, session: SessionBase):
        session["uid"] = self.uid

    @classmethod
    def clear(cls, session: SessionBase):
        del session["uid"]

    @classmethod
    def from_session(cls, session: SessionBase) -> SessionUser | None:
        if "uid" in session and (uid := session["uid"]) != "":
            return cls(uid)
        return None

    @classmethod
    def fromUser(cls, user: UserModel) -> SessionUser:
        return cls(user.uid)
