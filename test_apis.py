import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os
import json

from apis import app
from database import Base, get_db
from database import Plant, Product, Material, Order, PlantProduct, ProductMaterial

TEST_DB_URL = "sqlite:///./test.db"
engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(scope="function")
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_create_plant(setup_database):
    plant_data = {"name": "Test Plant", "location": "Test Location", "capacity": 100}
    response = client.post("/plants/", json=plant_data)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == plant_data["name"]
    assert data["location"] == plant_data["location"]
    assert data["capacity"] == plant_data["capacity"]
    assert "id" in data

def test_read_plants(setup_database):
    plant_data = {"name": "Test Plant", "location": "Test Location", "capacity": 100}
    client.post("/plants/", json=plant_data)
    
    response = client.get("/plants/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert any(plant["name"] == "Test Plant" for plant in data)

def test_read_plant(setup_database):
    plant_data = {"name": "Test Plant", "location": "Test Location", "capacity": 100}
    create_response = client.post("/plants/", json=plant_data)
    plant_id = create_response.json()["id"]
    
    response = client.get(f"/plants/{plant_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == plant_data["name"]
    assert data["id"] == plant_id

def test_update_plant(setup_database):

    plant_data = {"name": "Test Plant", "location": "Test Location", "capacity": 100}
    create_response = client.post("/plants/", json=plant_data)
    plant_id = create_response.json()["id"]
    
    
    updated_data = {"name": "Updated Plant", "location": "Updated Location", "capacity": 200}
    response = client.put(f"/plants/{plant_id}", json=updated_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == updated_data["name"]
    assert data["location"] == updated_data["location"]
    assert data["capacity"] == updated_data["capacity"]

def test_delete_plant(setup_database):
    plant_data = {"name": "Test Plant", "location": "Test Location", "capacity": 100}
    create_response = client.post("/plants/", json=plant_data)
    plant_id = create_response.json()["id"]
    
    # Now delete the plant
    response = client.delete(f"/plants/{plant_id}")
    assert response.status_code == 204
    
    # Try to get the deleted plant
    response = client.get(f"/plants/{plant_id}")
    assert response.status_code == 404

# Test product endpoints
def test_create_product(setup_database):
    product_data = {"name": "Test Product", "description": "Test Description", "category": "Test Category", "price": 99.99}
    response = client.post("/products/", json=product_data)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == product_data["name"]
    assert data["description"] == product_data["description"]
    assert "id" in data

def test_read_products(setup_database):
    # First, create a product
    product_data = {"name": "Test Product", "description": "Test Description", "category": "Test Category", "price": 99.99}
    client.post("/products/", json=product_data)
    
    # Now test getting all products
    response = client.get("/products/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert any(product["name"] == "Test Product" for product in data)

def test_update_product(setup_database):
    # First, create a product
    product_data = {"name": "Test Product", "description": "Test Description", "category": "Test Category", "price": 99.99}
    create_response = client.post("/products/", json=product_data)
    product_id = create_response.json()["id"]
    
    # Now update the product
    updated_data = {"name": "Updated Product", "description": "Updated Description", "category": "Updated Category", "price": 199.99}
    response = client.put(f"/products/{product_id}", json=updated_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == updated_data["name"]
    assert data["description"] == updated_data["description"]

# Test material endpoints
def test_create_material(setup_database):
    material_data = {"name": "Test Material", "description": "Test Description", "unit": "kg", "cost": 9.99}
    response = client.post("/materials/", json=material_data)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == material_data["name"]
    assert data["description"] == material_data["description"]
    assert "id" in data

def test_read_materials(setup_database):
    material_data = {"name": "Test Material", "description": "Test Description", "unit": "kg", "cost": 9.99}
    client.post("/materials/", json=material_data)
    
    response = client.get("/materials/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert any(material["name"] == "Test Material" for material in data)

def test_create_order(setup_database):
    order_data = {
        "order_date": datetime.now().isoformat(),
        "status": "Pending",
        "customer_name": "Test Customer"
    }
    response = client.post("/orders/", json=order_data)
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == order_data["status"]
    assert data["customer_name"] == order_data["customer_name"]
    assert "id" in data

def test_read_orders(setup_database):
    order_data = {
        "order_date": datetime.now().isoformat(),
        "status": "Pending",
        "customer_name": "Test Customer"
    }
    client.post("/orders/", json=order_data)
    
    response = client.get("/orders/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert any(order["customer_name"] == "Test Customer" for order in data)

def test_create_plant_product(setup_database):
    plant_data = {"name": "Test Plant", "location": "Test Location", "capacity": 100}
    plant_response = client.post("/plants/", json=plant_data)
    plant_id = plant_response.json()["id"]
    
    product_data = {"name": "Test Product", "description": "Test Description", "category": "Test Category", "price": 99.99}
    product_response = client.post("/products/", json=product_data)
    product_id = product_response.json()["id"]
    
    plant_product_data = {"plant_id": plant_id, "product_id": product_id, "quantity": 50}
    response = client.post("/plant-products/", json=plant_product_data)
    assert response.status_code == 201
    data = response.json()
    assert data["plant_id"] == plant_id
    assert data["product_id"] == product_id
    assert data["quantity"] == 50

def test_create_product_material(setup_database):
    product_data = {"name": "Test Product", "description": "Test Description", "category": "Test Category", "price": 99.99}
    product_response = client.post("/products/", json=product_data)
    product_id = product_response.json()["id"]
    
    material_data = {"name": "Test Material", "description": "Test Description", "unit": "kg", "cost": 9.99}
    material_response = client.post("/materials/", json=material_data)
    material_id = material_response.json()["id"]
    
    product_material_data = {"product_id": product_id, "material_id": material_id, "quantity": 5}
    response = client.post("/product-materials/", json=product_material_data)
    assert response.status_code == 201
    data = response.json()
    assert data["product_id"] == product_id
    assert data["material_id"] == material_id
    assert data["quantity"] == 5

def test_create_order_product(setup_database):
    order_data = {
        "order_date": datetime.now().isoformat(),
        "status": "Pending",
        "customer_name": "Test Customer"
    }
    order_response = client.post("/orders/", json=order_data)
    order_id = order_response.json()["id"]
    
    product_data = {"name": "Test Product", "description": "Test Description", "category": "Test Category", "price": 99.99}
    product_response = client.post("/products/", json=product_data)
    product_id = product_response.json()["id"]
    
    order_product_data = {"order_id": order_id, "product_id": product_id, "quantity": 10}
    response = client.post("/order-products/", json=order_product_data)
    assert response.status_code == 201
    data = response.json()
    assert data["order_id"] == order_id
    assert data["product_id"] == product_id
    assert data["quantity"] == 10

def test_create_storage_product(setup_database):
    product_data = {"name": "Test Product", "description": "Test Description", "category": "Test Category", "price": 99.99}
    product_response = client.post("/products/", json=product_data)
    product_id = product_response.json()["id"]
    
    storage_product_data = {"product_id": product_id, "quantity": 100}
    response = client.post("/storage-products/", json=storage_product_data)
    assert response.status_code == 201
    data = response.json()
    assert data["product_id"] == product_id
    assert data["quantity"] == 100

def test_create_storage_material(setup_database):
    material_data = {"name": "Test Material", "description": "Test Description", "unit": "kg", "cost": 9.99}
    material_response = client.post("/materials/", json=material_data)
    material_id = material_response.json()["id"]
    
    storage_material_data = {"material_id": material_id, "quantity": 500}
    response = client.post("/storage-materials/", json=storage_material_data)
    assert response.status_code == 201
    data = response.json()
    assert data["material_id"] == material_id
    assert data["quantity"] == 500

def test_full_order_flow(setup_database):
    material_data = {"name": "Raw Material", "description": "Basic Material", "unit": "kg", "cost": 5.00}
    material_response = client.post("/materials/", json=material_data)
    material_id = material_response.json()["id"]
    
    product_data = {"name": "Finished Product", "description": "End Product", "category": "Electronics", "price": 199.99}
    product_response = client.post("/products/", json=product_data)
    product_id = product_response.json()["id"]
    
    plant_data = {"name": "Manufacturing Plant", "location": "Factory District", "capacity": 1000}
    plant_response = client.post("/plants/", json=plant_data)
    plant_id = plant_response.json()["id"]
    
    # 4. Associate the material with the product (product requires materials)
    product_material_data = {"product_id": product_id, "material_id": material_id, "quantity": 2}
    client.post("/product-materials/", json=product_material_data)
    
    # 5. Associate the product with the plant (plant produces products)
    plant_product_data = {"plant_id": plant_id, "product_id": product_id, "quantity": 20}
    client.post("/plant-products/", json=plant_product_data)
    
    # 6. Add materials to storage
    storage_material_data = {"material_id": material_id, "quantity": 1000}
    client.post("/storage-materials/", json=storage_material_data)
    
    # 7. Add products to storage
    storage_product_data = {"product_id": product_id, "quantity": 50}
    client.post("/storage-products/", json=storage_product_data)
    
    # 8. Create an order
    order_data = {
        "order_date": datetime.now().isoformat(),
        "status": "New",
        "customer_name": "John Doe"
    }
    order_response = client.post("/orders/", json=order_data)
    order_id = order_response.json()["id"]
    
    # 9. Add products to the order
    order_product_data = {"order_id": order_id, "product_id": product_id, "quantity": 10}
    client.post("/order-products/", json=order_product_data)
    
    # 10. Update order status
    updated_order_data = {
        "order_date": datetime.now().isoformat(),
        "status": "Completed",
        "customer_name": "John Doe"
    }
    update_response = client.put(f"/orders/{order_id}", json=updated_order_data)
    assert update_response.status_code == 200
    assert update_response.json()["status"] == "Completed"
    
    # 11. Verify we can retrieve the order
    get_response = client.get(f"/orders/{order_id}")
    assert get_response.status_code == 200
    order_data = get_response.json()
    assert order_data["id"] == order_id
    assert order_data["status"] == "Completed"
    assert order_data["customer_name"] == "John Doe"

if __name__ == "__main__":
    pytest.main(["-vv"])