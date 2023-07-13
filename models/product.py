from typing import Optional
from sqlmodel import Field, Relationship, SQLModel
from models.user import User

class Category(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True)
    description: str
    name: str
    product: Optional['Product'] = Relationship(back_populates='category')

class Product(SQLModel, table = True):
    id: Optional[int] = Field(primary_key=True)
    description: str
    value: float
    qty: int
    name: str
    category_id: Optional[int] = Field(default=None, foreign_key='category.id')
    category: Optional[Category] = Relationship(back_populates='product')
    seller_id: Optional[int] = Field(default=None, foreign_key='user.id')
    seller: Optional[User] = Relationship()

