from datetime import datetime, timedelta
from fastapi import Request, HTTPException, Depends
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from database.database import get_db
from database.models import Account

SECRET_KEY = "tajny_klucz_produkcyjny"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
COOKIE_NAME = "open_space_auth"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def veryfy_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_account(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get(COOKIE_NAME)
    if not token:
        raise HTTPException(status_code=401, detail="NOT AUTHORIZED")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="INVALID TOKEN")
    except JWTError:
        raise HTTPException(status_code=401, detail="TOKEN VERIFICATION ERROR")

    account = db.query(Account).filter(Account.email == email).first()
    if email is None:
        raise HTTPException(status_code=401, detail="ACCOUNT NOT FOUND")

    return account
