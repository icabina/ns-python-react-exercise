from typing import List
from fastapi import APIRouter, Query, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.crud import crud_transaction
from app.schemas.transaction import TransactionCreate, TransactionUpdate, TransactionInDB, TransactionListItem, TransactionGridResponse, TransactionGridItem
from app.db.session import get_db

router = APIRouter()

@router.post("/transactions/", response_model=TransactionInDB)
def create_new_transaction(transaction: TransactionCreate, db: Session = Depends(get_db)):
    return crud_transaction.create_transaction(db=db, transaction=transaction, user_id=1)

@router.get("/transactions/", response_model=List[TransactionListItem])
def read_transactions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    transactions = crud_transaction.get_transactions(db, skip=skip, limit=limit)
    return transactions

@router.get("/transactions/grid-view", response_model=TransactionGridResponse)
def get_transactions_grid(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1),
    sort_by: str = Query("id"),
    sort_order: str = Query("asc"),
    db: Session = Depends(get_db),
):
    # Validate sort_order
    sort_order = sort_order.lower()
    if sort_order not in ("asc", "desc"):
        sort_order = "asc"

    # Map sort_by to real SQL columns
    column_map = {
        "id": "t.id",
        "description": "t.description",
        "amount": "t.amount",
        "type": "t.type",
        "date": "t.date",
        "category_name": "c.name"
    }

    sql_sort_column = column_map.get(sort_by, "t.id")

    # Raw SQL query with JOINs
    sql = text(f"""
        SELECT 
            t.id AS transaction_id,
            t.description,
            t.amount,
            t.type,
            t.date,
            t.category_id,
            c.name AS category_name,
            STRING_AGG(tag.name, ',') AS tags
        FROM transactions t
        LEFT JOIN categories c ON t.category_id = c.id
        LEFT JOIN transaction_tags tt ON t.id = tt.transaction_id
        LEFT JOIN tags tag ON tt.tag_id = tag.id
        GROUP BY t.id, c.name
        ORDER BY {sql_sort_column} {sort_order}
        LIMIT :limit OFFSET :offset
    """)

    offset = (page - 1) * size
    result = db.execute(sql, {"limit": size, "offset": offset}).fetchall()

    # Total count for pagination
    count_sql = text("SELECT COUNT(*) FROM transactions")
    total_count = db.execute(count_sql).scalar()

    # transform SQL results into list of TransactionGridItem dicts
    transactions = [
        TransactionGridItem(
            id=row.transaction_id,
            description=row.description,
            amount=row.amount,
            type=row.type,
            date=str(row.date),
            category_id=row.category_id,
            category_name=row.category_name,
            tags=row.tags.split(",") if row.tags else []
        )
        for row in result
    ]

    return TransactionGridResponse(
        data=transactions,
        total=total_count,
        page=page,
        size=size
    )

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

