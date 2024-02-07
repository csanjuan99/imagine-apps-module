import models.User as User
from schemas.User import User as UserModel
from sqlalchemy.orm import Session


def get_user_by_email(db: Session, email: str) -> UserModel:
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, email: str, password: str):
    db_user = User(email=email, password=password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
