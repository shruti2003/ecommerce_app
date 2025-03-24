    # POST /orders → Customer places an order

    # GET /orders/{id} → Fetch order details

    # PUT /orders/{id} → Admin updates order status

from fastapi import APIRouter, Depends, HTTPException, status
from app.database.db import get_db
from app.models.product import Product
from app.schemas import schemas
from app.models.order import Order
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/orders",
    tags=["orders"],
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model = schemas.OrderOut)
def createOrder(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    try:
        total_price = 0.0
        for product in order.products: 
            val = db.query(Product).filter(Product.id == product).first()
            total_price = val.price

        new_product = Order(
            customer_name=order.customer_name,
            customer_email=order.customer_email, 
            products = order.products,
            total_price=total_price
        )

        db.add(new_product)
        db.commit()
        db.refresh(new_product)

        return new_product
    except ValueError as e:
        raise HTTPException(status_code=422, detail=f"Invalid input: {str(e)}")
    
# GET /orders/{id} → Fetch order details


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.OrderOut)
def get_order(id: int, db: Session = Depends(get_db)):
    try:
        order = db.query(Order).filter(Order.id == id).first()

        return order

    except ValueError as e:
        raise HTTPException(status_code=422, detail=f"Invalid input: {str(e)}")
     



# PUT /orders/{id} → Admin updates order status

@router.put("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def update_product(id: int, updated_order: schemas.OrderCreate, db: Session = Depends(get_db)):
    try:
        order = db.query(Order).filter(Order.id == id)
        first_order = order.first()

        if not first_order:
            raise HTTPException(status_code=404, detail="Order not found")        

        order.update(updated_order.model_dump(), synchronize_session=False)
        
        db.commit()

        return {"message": "Order successfully updated"}

    except ValueError as e:
        raise HTTPException(status_code=422, detail=f"Invalid input: {str(e)}")
