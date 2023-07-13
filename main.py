from fastapi import Depends, FastAPI, HTTPException, status
import uvicorn
from models.product import *
from controller.productsController import product_router
from controller.userController import user_router

app = FastAPI()

app.include_router(product_router)
app.include_router(user_router)


if __name__ == '__main__':
    uvicorn.run('main:app', host="localhost", port=8000, reload=True)
    #create_db_and_tables()