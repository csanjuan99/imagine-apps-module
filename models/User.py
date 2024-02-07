from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from sql_app.database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password = Column(String(500), nullable=False)
    tasks = relationship('Task', back_populates='user')
