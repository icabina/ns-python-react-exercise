from sqlalchemy.orm import Session, joinedload
from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate, TransactionUpdate, TransactionListItem
from app.models.category import Category
from sqlalchemy.orm import selectinload
from typing import List

def get_transaction(db: Session, transaction_id: int):
    return db.query(Transaction).filter(Transaction.id == transaction_id).first()

def get_transactions(db: Session, skip: int = 0, limit: int = 100) -> List[TransactionListItem]:
    results = (
        db.query(
            Transaction.id,
            Transaction.description,
            Transaction.amount,
            Transaction.type,
            Transaction.category_id,
            Category.name.label("category_name"),
            Transaction.date
        )
        .join(Category, Transaction.category_id == Category.id)
        .offset(skip)
        .limit(limit)
        .all()
    )

    return [
        TransactionListItem(
            id=r[0],
            description=r[1],
            amount=r[2],
            type=r[3],
            category_id=r[4],
            category_name=r[5],
            date=r[6]
        )
        for r in results
    ]

def create_transaction(db: Session, transaction: TransactionCreate, user_id: int):
    db_transaction = Transaction(**transaction.model_dump(), user_id=user_id)
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

def update_transaction(db: Session, transaction_id: int, transaction: TransactionUpdate):
    db_transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if db_transaction:
        for key, value in transaction.model_dump().items():
            setattr(db_transaction, key, value)
        db.commit()
        db.refresh(db_transaction)
    return db_transaction

def delete_transaction(db: Session, transaction_id: int):
    db_transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if db_transaction:
        db.delete(db_transaction)
        db.commit()
    return db_transaction