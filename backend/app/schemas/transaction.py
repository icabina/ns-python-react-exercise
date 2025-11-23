from datetime import datetime
from pydantic import BaseModel, ConfigDict
from .category import Category

class TransactionBase(BaseModel):
    description: str
    amount: float
    type: str
    category_id: int
    user_id: int

class TransactionCreate(TransactionBase):
    pass

class TransactionUpdate(TransactionBase):
    pass

class TransactionInDBBase(BaseModel):
    id: int
    description: str
    amount: float
    type: str
    category_id: int
    user_id: int
    date: datetime

    model_config = ConfigDict(from_attributes=True)

class TransactionInDB(TransactionInDBBase):
    category_rel: Category

class TransactionListItem(BaseModel):
    id: int
    description: str
    amount: float
    type: str
    category_id: int
    category_name: str
    date: datetime

