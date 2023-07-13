from typing import List, Dict, Union

from fastapi import APIRouter, Security, security, Depends, Query
from fastapi.security import HTTPAuthorizationCredentials
from sqlmodel import select
from starlette.responses import JSONResponse
from starlette.status import HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND, HTTP_401_UNAUTHORIZED
from fastapi.encoders import jsonable_encoder
import repository.products
from controller.userController import auth_handler
from models.product import *
from database.db import session

product_router = APIRouter()


@product_router.get('/')
def test():
    return 'Hello Lucas'


@product_router.get('/products', tags=['Products'])
def products():
    products = select(Product, Category).join(Category)
    products = session.exec(products).all()
    return {'products': products}


@product_router.get('/product/{id}', response_model=Product, tags=['Products'])
def product(id: int):
    products_found = session.get(Product, id)
    if not products_found:
        return JSONResponse(content=HTTP_404_NOT_FOUND)
    return products_found


@product_router.post('/products', tags=['Products'])
def createProduct(cat: Category, prod: Product, user=Depends(auth_handler.get_current_user)):
    if not user.is_seller:
        return JSONResponse(content=HTTP_401_UNAUTHORIZED)

    categories = Category(
        name=cat.name, 
        description=cat.description
    )
    session.add(categories)
    session.commit()
    product = Product(
        description=prod.description,
        value=prod.value,
        qty=prod.qty,
        name=prod.name,
        category_id=categories.id,
        category=categories,
        seller_id=user.id, 
        seller=user
    )
    session.add(product)
    session.commit()
    return prod


@product_router.put('/products/{id}', response_model=Product, tags=['Products'])
def updateProduct(id: int, prod: Product, user=Depends(auth_handler.get_current_user)):
    productFound = session.get(Product, id)
    if not user.is_seller or productFound.seller_id != user.id:
        return JSONResponse(content=HTTP_401_UNAUTHORIZED)
    update_item_encoded = jsonable_encoder(prod)
    update_item_encoded.pop('id', None)
    for key, val in update_item_encoded.items():
        productFound.__setattr__(key, val)
    session.commit()
    return productFound


@product_router.delete('/products/{id}', status_code=HTTP_204_NO_CONTENT, tags=['Products'])
def delete_gem(id:int, user=Depends(auth_handler.get_current_user)):
    productFound = session.get(Product, id)
    if not user.is_seller or productFound.seller_id != user.id:
        return JSONResponse(content=HTTP_401_UNAUTHORIZED)
    session.delete(productFound)
    session.commit()