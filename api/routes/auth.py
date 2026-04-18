from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta

router = APIRouter()

SECRET = "supersecret"
ALGO = "HS256"

pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto"
)
# In-memory store
fake_users = {}


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
    if user.email in fake_users:
        raise HTTPException(status_code=400, detail="User exists")

    fake_users[user.email] = hash_password(user.password)
    return {"msg": "registered"}


@router.post("/login")
def login(user: UserIn):
    stored = fake_users.get(user.email)

    if not stored or not verify_password(user.password, stored):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_token({"sub": user.email})
    return {"access_token": token}
