from sqlmodel import Session, select

from database.db import engine
from models.user import User


def selectAllUsers():
    with Session(engine) as session:
        statement = select(User)
        res = session.exec(statement).all()
        return res


def findUser(name):
    with Session(engine) as session:
        statement = select(User).where(User.username == name)
        return session.exec(statement).first()