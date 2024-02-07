from fastapi import APIRouter, Depends
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import services.AuthService as AuthService
from sqlalchemy.orm import Session
from sql_app.database import get_db
from schemas.User import UserCreate, User

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


@router.post("/auth/register", response_model=User)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    return await AuthService.register(db, user.email, user.password, user.repeat_password)


@router.post("/auth/login")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    return await AuthService.login(db, form_data.username, form_data.password)


@router.get("/auth/user")
async def user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    return await AuthService.me(db, token)
