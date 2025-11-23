from datetime import datetime
from pydantic import BaseModel, ConfigDict
from .category import Category
from .tag import Tag
from typing import List

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
    tags: list[Tag] = []

class TransactionListItem(BaseModel):
    id: int
    description: str
    amount: float
    type: str
    category_id: int
    category_name: str
    date: datetime

class TransactionGridItem(BaseModel):
    id: int
    description: str
    amount: float
    type: str
    date: str
    category_id: int
    category_name: str
    tags: List[str]

class TransactionGridResponse(BaseModel):
    data: List[TransactionGridItem]
    total: int
    page: int
    size: int


