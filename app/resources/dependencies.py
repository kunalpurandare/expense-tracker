# app/dependencies.py

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from ..database.database import SessionLocal
from ..database import models
from . import auth, crud

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")


# 📦 Reusable DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 🔐 Get current user from JWT token
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> models.User:
    payload = auth.decode_access_token(token)
    username = payload.get("sub")
    role = payload.get("role")
    if username is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user = crud.get_user_by_username(db, username)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def require_admin(current_user: models.User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admins only")
    return current_user
