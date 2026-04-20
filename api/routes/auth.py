from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from app.db.user_repo import create_user, get_user_by_email
router = APIRouter()

SECRET = "" ##add a random ahh secret keyword here
ALGO = "HS256"

pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto"
)


class UserIn(BaseModel):
    email: str
    password: str

def hash_password(pw: str):
    return pwd_context.hash(pw[:72])

def verify_password(pw: str, hashed: str):
    return pwd_context.verify(pw[:72], hashed)

def create_token(data: dict):
    payload = data.copy()
    payload["exp"] = datetime.utcnow() + timedelta(hours=24)
    return jwt.encode(payload, SECRET, algorithm=ALGO)


@router.post("/register")
def register(user: UserIn):
    existing = get_user_by_email(user.email)

    if existing:
        raise HTTPException(status_code=400, detail="User exists")

    hashed = hash_password(user.password)

    create_user(user.email, hashed)

    return {"msg": "registered"}

@router.post("/login")
def login(user: UserIn):
    db_user = get_user_by_email(user.email)

    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(user.password, db_user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_token({
        "sub": db_user["email"],
        "user_id": db_user["id"]
    })

    return {"access_token": token}

def decode_token(token: str):
    return jwt.decode(token, SECRET, algorithms=[ALGO])
