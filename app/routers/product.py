import random
import datetime
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status, HTTPException
from app import models
from app.models.product import Product
from app.schemas import schemas
from app.database.db import get_db
from app.models.user import User
from app.utils.hash_password import hash  

router = APIRouter(
    prefix="/products",
    tags=["products"],
)

@router.get("/all", status_code=status.HTTP_200_OK)
def get_products(db: Session = Depends(get_db)):
    try: 
        products = db.query(Product).all()
        if products:
            return products
        else:
            raise HTTPException(status_code=404, detail="products not found")

    except ValueError as e:
        raise HTTPException(status_code=404, detail=f"Invalid input: {str(e)}")


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.ProductOut)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    try:
        new_product = Product(
            name=product.name,
            description=product.description, 
            price=product.price, 
            stock_quantity=product.stock_quantity
        )

        db.add(new_product)
        db.commit()
        db.refresh(new_product)

        return new_product
    except ValueError as e:
        raise HTTPException(status_code=422, detail=f"Invalid input: {str(e)}")


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(id: int, db: Session = Depends(get_db)):
    try:
        product = db.query(Product).filter(Product.id == id).first()

        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        db.delete(product)
        db.commit()

        return {"message": "Product successfully deleted"}

    except ValueError as e:
        raise HTTPException(status_code=422, detail=f"Invalid input: {str(e)}")


@router.put("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def update_product(id: int, updated_product: schemas.ProductCreate, db: Session = Depends(get_db)):
    try:
        product = db.query(Product).filter(Product.id == id)
        first_product = product.first()

        if not first_product:
            raise HTTPException(status_code=404, detail="Product not found")        

        product.update(updated_product.model_dump(), synchronize_session=False)
        
        db.commit()

        return {"message": "Product successfully updated"}

    except ValueError as e:
        raise HTTPException(status_code=422, detail=f"Invalid input: {str(e)}")
