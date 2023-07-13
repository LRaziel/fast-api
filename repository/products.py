from database.db import engine
from models.product import Product, Category
from sqlmodel import Session, select, or_


def selectAllProducts():
    with Session(engine) as session:
        statement = select(Product, Category).join(Category)
        result = session.exec(statement)
        res = []
        for product, cat in result:
            res.append({'product': product, 'category': cat})
        return res


def selectProductById(id):
    with Session(engine) as session:
        statement = select(Product, Category).join(Category)
        statement = statement.where(Product.id==id)
        result = session.exec(statement)
        return result.first()