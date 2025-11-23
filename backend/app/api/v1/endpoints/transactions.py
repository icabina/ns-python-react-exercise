from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud import crud_transaction
from app.schemas.transaction import TransactionCreate, TransactionUpdate, TransactionInDB, TransactionListItem
from app.db.session import get_db

router = APIRouter()

@router.post("/transactions/", response_model=TransactionInDB)
def create_new_transaction(transaction: TransactionCreate, db: Session = Depends(get_db)):
    return crud_transaction.create_transaction(db=db, transaction=transaction, user_id=1)

@router.get("/transactions/", response_model=List[TransactionListItem])
def read_transactions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    transactions = crud_transaction.get_transactions(db, skip=skip, limit=limit)
    return transactions

@router.get("/transactions/{transaction_id}", response_model=TransactionInDB)
def read_transaction(transaction_id: int, db: Session = Depends(get_db)):
    transaction = crud_transaction.get_transaction(db, transaction_id=transaction_id)
    if transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction

@router.put("/transactions/{transaction_id}", response_model=TransactionInDB)
def update_existing_transaction(
    transaction_id: int, transaction: TransactionUpdate, db: Session = Depends(get_db)
):
    db_transaction = crud_transaction.update_transaction(db, transaction_id, transaction)
    if db_transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return db_transaction

@router.delete("/transactions/{transaction_id}", response_model=TransactionInDB)
def delete_existing_transaction(transaction_id: int, db: Session = Depends(get_db)):
    db_transaction = crud_transaction.delete_transaction(db, transaction_id)
    if db_transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return db_transaction
