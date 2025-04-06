from sqlalchemy.orm import Session
from ..database import models, schemas
from typing import List

# ----- User CRUD -----

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate, hashed_password: str):
    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        role=user.role or "user"
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# ----- Transaction CRUD -----

def create_transaction(db: Session, transaction: schemas.TransactionCreate, user_id: int):
    db_transaction = models.Transaction(**transaction.dict(), user_id=user_id)
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

def get_transactions(db: Session, user_id: int) -> List[models.Transaction]:
    return db.query(models.Transaction).filter(models.Transaction.user_id == user_id).all()

def get_transaction(db: Session, transaction_id: int, user_id: int):
    return db.query(models.Transaction).filter(
        models.Transaction.id == transaction_id,
        models.Transaction.user_id == user_id
    ).first()

def update_transaction(db: Session, db_transaction: models.Transaction, updated_data: schemas.TransactionCreate):
    for key, value in updated_data.dict().items():
        setattr(db_transaction, key, value)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

def delete_transaction(db: Session, db_transaction: models.Transaction):
    db.delete(db_transaction)
    db.commit()

def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def delete_user(db: Session, user: models.User):
    db.delete(user)
    db.commit()

def get_all_users(db: Session):
    return db.query(models.User).all()

def get_all_transactions(db: Session):
    return db.query(models.Transaction).all()
