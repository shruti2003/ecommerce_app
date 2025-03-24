# import pytest
# from fastapi.testclient import TestClient
# from app.main import app  # Import your FastAPI app
# from app.database.db import get_db, Base  # Ensure you import Base for table creation
# from app.models.product import Product
# from app.models.order import Order
# from app.schemas import schemas
# from unittest.mock import patch
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker

# # Setup for testing database (mock database setup)
# SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
# engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
# TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# # Dependency to override get_db during testing
# def override_get_db():
#     db = TestingSessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# # Use FastAPI's TestClient to make requests to the application
# @pytest.fixture(scope="module")
# def client():
#     # Create tables in the test database
#     Base.metadata.create_all(bind=engine)
    
#     app.dependency_overrides[get_db] = override_get_db
#     with TestClient(app) as client:
#         yield client

#     # Cleanup: Drop tables after tests are finished
#     Base.metadata.drop_all(bind=engine)

# @pytest.fixture(scope="module")
# def create_mock_data(client):
#     db = TestingSessionLocal()

#     # Add a sample product for testing
#     product = Product(name="Product1", price=100.0, stock_quantity=10)
#     db.add(product)
#     db.commit()
#     db.refresh(product)

#     # Add an order that references the created product
#     order = Order(
#         customer_name="Test Customer",
#         customer_email="test@customer.com",
#         products=[product.id],
#         total_price=100.0
#     )
#     db.add(order)
#     db.commit()
#     db.refresh(order)

#     return order, product


# ### Tests for POST /orders
# def test_create_order(client, create_mock_data):
#     order, _ = create_mock_data
#     order_data = {
#         "customer_name": "New Customer",
#         "customer_email": "new@customer.com",
#         "products": [order.products[0]],
#     }
#     response = client.post("/orders/", json=order_data)

#     assert response.status_code == 201
#     data = response.json()
#     assert data["customer_name"] == order_data["customer_name"]
#     assert data["customer_email"] == order_data["customer_email"]

# ### Tests for GET /orders/{id}
# def test_get_order(client, create_mock_data):
#     order, _ = create_mock_data
#     response = client.get(f"/orders/{order.id}")
    
#     assert response.status_code == 200
#     data = response.json()
#     assert data["id"] == order.id
#     assert data["customer_name"] == order.customer_name
#     assert data["customer_email"] == order.customer_email

# ### Tests for PUT /orders/{id}
# def test_update_order(client, create_mock_data):
#     order, product = create_mock_data
#     updated_order_data = {
#         "customer_name": "Updated Customer",
#         "customer_email": "updated@customer.com",
#         "products": [product.id],
#     }
    
#     # Admin authentication mock
#     with patch("app.auth.auth.get_current_admin_user") as mock_admin:
#         mock_admin.return_value = {"id": 1, "role": "admin"}  # Mock admin user
#         response = client.put(f"/orders/{order.id}", json=updated_order_data)

#     assert response.status_code == 204
#     # Fetch the updated order and verify changes
#     updated_order = client.get(f"/orders/{order.id}").json()
#     assert updated_order["customer_name"] == updated_order_data["customer_name"]
#     assert updated_order["customer_email"] == updated_order_data["customer_email"]
