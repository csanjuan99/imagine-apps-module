from .User import User
from .Task import Task
from sql_app.database import Base
from sql_app.database import engine


def __init__():
    Base.metadata.create_all(bind=engine)
