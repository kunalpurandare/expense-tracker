# app/routers/admin.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..database import models, schemas
from ..resources import crud
from ..resources.dependencies import get_db, require_admin

router = APIRouter(prefix="/admin", tags=["Admin"])


# 🚫 Delete any user by ID (admin only)
@router.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db), admin: models.User = Depends(require_admin)):
    user = crud.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    crud.delete_user(db, user)
    return {"detail": f"User {user.username} deleted successfully"}


# 👀 Get all users (admin only)
@router.get("/users", response_model=List[schemas.User])
def list_all_users(db: Session = Depends(get_db), admin: models.User = Depends(require_admin)):
    return crud.get_all_users(db)


# 👀 Get all transactions across users
@router.get("/transactions", response_model=List[schemas.Transaction])
def list_all_transactions(db: Session = Depends(get_db), admin: models.User = Depends(require_admin)):
    return crud.get_all_transactions(db)
