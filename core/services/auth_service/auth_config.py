import os
import hmac
import hashlib
from datetime import datetime, timedelta

from fastapi import Request, HTTPException, Depends, Response
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from database.database import get_db
from database.models import Account


# JWT config

SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-insecure-secret")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
COOKIE_NAME = "open_space_auth"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="account/login", auto_error=False)


# Password hashing config

# Argon2id preferred + bcrypt for old hashes.
pwd_context = CryptContext(
    schemes=["argon2", "bcrypt"],
    deprecated=["bcrypt"],  # bcrypt hashes will be rehashed to argon2 after login
    argon2__type="ID",
    argon2__time_cost=3,
    argon2__memory_cost=65536,
    argon2__parallelism=2,
    bcrypt__rounds=12,
)


def _get_pepper() -> bytes:
    """
    Pepper = server secret used before hashing.
    Required in production-like environments.
    """
    env = os.getenv("ENVIRONMENT", "development").lower()
    pepper = os.getenv("HASHING_PEPPER")

    if pepper:
        return pepper.encode("utf-8")

    # allow default only in dev/test so project runs easily
    if env in ("development", "dev", "test"):
        return b"dev-unsafe-pepper"

    raise RuntimeError("HASHING_PEPPER is missing. Set it in your environment.")


def _pepper_input(value: str) -> str:
    """
    HMAC(pepper, password) -> hex string.
    Then we hash that output with Argon2id/bcrypt.
    """
    return hmac.new(_get_pepper(), value.encode("utf-8"), hashlib.sha256).hexdigest()


# REQUIRED password API
def hash_password(plain: str) -> str:
    if not plain:
        raise ValueError("Password must not be empty")
    return pwd_context.hash(_pepper_input(plain))


def verify_password(plain_password: str, hashed_password: str) -> bool:
    if not plain_password or not hashed_password:
        return False
    try:
        return pwd_context.verify(_pepper_input(plain_password), hashed_password)
    except Exception:
        return False


def needs_rehash(hashed_password: str) -> bool:
    if not hashed_password:
        return False
    try:
        return pwd_context.needs_update(hashed_password)
    except Exception:
        return True


# Backwards-compatible name used by your register code
def get_password_hash(password: str) -> str:
    return hash_password(password)


# JWT helpers
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def set_auth_cookie(response: Response, access_token: str):
    response.set_cookie(
        key=COOKIE_NAME,
        value=access_token,
        httponly=True,
        samesite="lax",
        secure=False,  # set True behind HTTPS in production
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        expires=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )


def get_current_account(
    request: Request,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    if not token:
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
    if account is None:
        raise HTTPException(status_code=401, detail="ACCOUNT NOT FOUND")

    return account
