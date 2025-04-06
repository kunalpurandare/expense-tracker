from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import models ,schemas
from ..resources import crud
from ..resources.dependencies import get_db, get_current_user

router = APIRouter(prefix="/transactions", tags=["Transactions"])

@router.post("/", response_model=schemas.Transaction)
def create(transaction: schemas.TransactionCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return crud.create_transaction(db, transaction, current_user.id)


@router.get("/", response_model=List[schemas.Transaction])
def get_all(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return crud.get_transactions(db, current_user.id)


@router.get("/{transaction_id}", response_model=schemas.Transaction)
def get(transaction_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    transaction = crud.get_transaction(db, transaction_id, current_user.id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction


@router.put("/{transaction_id}", response_model=schemas.Transaction)
def update(transaction_id: int, updated_data: schemas.TransactionCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    transaction = crud.get_transaction(db, transaction_id, current_user.id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return crud.update_transaction(db, transaction, updated_data)


@router.delete("/{transaction_id}")
def delete(transaction_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    transaction = crud.get_transaction(db, transaction_id, current_user.id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    crud.delete_transaction(db, transaction)
    return {"detail": "Transaction deleted"}

# Filter and summary endpoints remain as-is (you can also abstract them later if needed)

from fastapi import Query
from datetime import date

@router.get("/filter/", response_model=List[schemas.Transaction])
def filter_transactions(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
    category: str | None = None,
    type: models.TransactionType | None = None,
    start_date: date | None = None,
    end_date: date | None = None
):
    query = db.query(models.Transaction).filter(models.Transaction.user_id == current_user.id)

    if category:
        query = query.filter(models.Transaction.category == category)
    if type:
        query = query.filter(models.Transaction.type == type)
    if start_date and end_date:
        query = query.filter(models.Transaction.date.between(start_date, end_date))

    return query.all()

from sqlalchemy import func
from collections import defaultdict

# Monthly Summary
@router.get("/summary/monthly/", response_model=dict)
def get_monthly_summary(
    year: int,
    month: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    income = db.query(func.sum(models.Transaction.amount)).filter(
        models.Transaction.user_id == current_user.id,
        models.Transaction.type == models.TransactionType.income,
        func.extract('year', models.Transaction.date) == year,
        func.extract('month', models.Transaction.date) == month
    ).scalar() or 0

    expense = db.query(func.sum(models.Transaction.amount)).filter(
        models.Transaction.user_id == current_user.id,
        models.Transaction.type == models.TransactionType.expense,
        func.extract('year', models.Transaction.date) == year,
        func.extract('month', models.Transaction.date) == month
    ).scalar() or 0

    return {"year": year, "month": month, "income": income, "expense": expense}

# Category-wise Summary
@router.get("/summary/category/", response_model=dict)
def get_category_summary(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    category_totals = defaultdict(lambda: {"income": 0, "expense": 0})

    transactions = db.query(models.Transaction).filter(models.Transaction.user_id == current_user.id).all()

    for transaction in transactions:
        category_totals[transaction.category][transaction.type] += transaction.amount

    return category_totals
