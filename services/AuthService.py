from repository import UserRepository
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from passlib.context import CryptContext
from datetime import timedelta, timezone, datetime
from jose import JWTError, jwt

# This secret key should be in a .env file,
# but for the sake of simplicity, I'll leave it here
SECRET_KEY = "$2a$14$vrrYXC86E4dVkMYS0C0r1O8zPO8Uha6s8MA8rJPbeU38IqYSIS.qy"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


async def login(db: Session, email: str, password: str):
    user = UserRepository.get_user_by_email(email=email, db=db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    is_password_valid = pwd_context.verify(password, user.password)
    if not is_password_valid:
        raise HTTPException(status_code=400, detail="Incorrect password")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"sub": user.email}
    if access_token_expires:
        expire = datetime.now(timezone.utc) + access_token_expires
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return {
        "access_token": encoded_jwt,
        "token_type": "bearer"
    }


async def register(db: Session, email: str, password: str, repeat_password: str):
    user = UserRepository.get_user_by_email(email=email, db=db)
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")
    if password != repeat_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    hash_password = pwd_context.hash(password)
    return UserRepository.create_user(db=db, email=email, password=hash_password)


async def me(db: Session, token: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        user = UserRepository.get_user_by_email(db, email)
    except JWTError:
        raise credentials_exception

    if user is None:
        raise credentials_exception
    return user
