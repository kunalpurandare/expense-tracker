from typing import Optional
from pydantic import BaseModel, EmailStr
from enum import Enum
from datetime import datetime

from .models import TransactionType

# User schemas
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: Optional[str] = "user"

class User(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        orm_mode = True

# Token
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    username: str | None = None

class TransactionCreate(BaseModel):
    amount: float
    category: str
    type: TransactionType
    note: str | None = None
    date: datetime = datetime.utcnow()

class Transaction(TransactionCreate):
    id: int
    user_id: int

    class Config:
        orm_mode = True

