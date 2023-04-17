from __future__ import annotations
from App.models import UserModel


class SessionUser:
    def __init__(self, uid: str, email: str):
        assert uid != "", "uid is empty"
        self.uid: str | None = uid
        self.email: str | None = email

    def save(self, session):
        session["uid"] = self.uid
        session["email"] = self.email

    def dict(self):
        return {"uid": self.uid, "email": self.email}

    @classmethod
    def clear(cls, session):
        del session["uid"]
        del session["email"]

    @classmethod
    def from_session(cls, session) -> SessionUser | None:
        if "uid" in session and (uid := session["uid"]) != "":
            return cls(uid, session["email"])
        return None

    @classmethod
    def fromUser(cls, user: UserModel) -> SessionUser:
        return cls(str(user.uid), user.email)
