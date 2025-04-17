from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel  


import schemas
from database import get_db, Plant, Product, Material, Order, PlantProduct, PlantMaterial
from database import StorageProduct, StorageMaterial, ProductMaterial, OrderProduct

app = FastAPI(title="Manufacturing Management API", 
              description="API for managing plants, products, materials, and orders")

# Define models for join tables (moved to the top before they're used)
class PlantProductCreate(BaseModel):
    plant_id: int
    product_id: int
    quantity: Optional[int] = None

class PlantMaterialCreate(BaseModel):
    plant_id: int
    material_id: int
    quantity: Optional[int] = None

class ProductMaterialCreate(BaseModel):
    product_id: int
    material_id: int
    quantity: int

class OrderProductCreate(BaseModel):
    order_id: int
    product_id: int
    quantity: int

class StorageProductCreate(BaseModel):
    product_id: int
    quantity: int

class StorageMaterialCreate(BaseModel):
    material_id: int
    quantity: int

@app.get('/')
async def root():
    return {'message': 'Welcome!'}

# Plant CRUD Operations
@app.post("/plants/", response_model=schemas.Plant, status_code=status.HTTP_201_CREATED)
def create_plant(plant: schemas.PlantCreate, db: Session = Depends(get_db)):
    db_plant = Plant(name=plant.name, location=plant.location, capacity=plant.capacity)
    db.add(db_plant)
    db.commit()
    db.refresh(db_plant)
    return db_plant

@app.get("/plants/", response_model=List[schemas.Plant])
def read_plants(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    plants = db.query(Plant).offset(skip).limit(limit).all()
    return plants

@app.get("/plants/{plant_id}", response_model=schemas.Plant)
def read_plant(plant_id: int, db: Session = Depends(get_db)):
    plant = db.query(Plant).filter(Plant.id == plant_id).first()
    if plant is None:
        raise HTTPException(status_code=404, detail="Plant not found")
    return plant

@app.put("/plants/{plant_id}", response_model=schemas.Plant)
def update_plant(plant_id: int, plant: schemas.PlantCreate, db: Session = Depends(get_db)):
    db_plant = db.query(Plant).filter(Plant.id == plant_id).first()
    if db_plant is None:
        raise HTTPException(status_code=404, detail="Plant not found")
    
    for key, value in plant.dict().items():
        setattr(db_plant, key, value)
    
    db.commit()
    db.refresh(db_plant)
    return db_plant

@app.delete("/plants/{plant_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_plant(plant_id: int, db: Session = Depends(get_db)):
    db_plant = db.query(Plant).filter(Plant.id == plant_id).first()
    if db_plant is None:
        raise HTTPException(status_code=404, detail="Plant not found")
    
    db.delete(db_plant)
    db.commit()
    return None

# Product CRUD Operations
@app.post("/products/", response_model=schemas.Product, status_code=status.HTTP_201_CREATED)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    db_product = Product(
        name=product.name,
        description=product.description,
        category=product.category,
        price=product.price
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@app.get("/products/", response_model=List[schemas.Product])
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    products = db.query(Product).offset(skip).limit(limit).all()
    return products

@app.get("/products/{product_id}", response_model=schemas.Product)
def read_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.put("/products/{product_id}", response_model=schemas.Product)
def update_product(product_id: int, product: schemas.ProductCreate, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    
    for key, value in product.dict().items():
        setattr(db_product, key, value)
    
    db.commit()
    db.refresh(db_product)
    return db_product

@app.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    
    db.delete(db_product)
    db.commit()
    return None

# Material CRUD Operations
@app.post("/materials/", response_model=schemas.Material, status_code=status.HTTP_201_CREATED)
def create_material(material: schemas.MaterialCreate, db: Session = Depends(get_db)):
    db_material = Material(
        name=material.name,
        description=material.description,
        unit=material.unit,
        cost=material.cost
    )
    db.add(db_material)
    db.commit()
    db.refresh(db_material)
    return db_material

@app.get("/materials/", response_model=List[schemas.Material])
def read_materials(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    materials = db.query(Material).offset(skip).limit(limit).all()
    return materials

@app.get("/materials/{material_id}", response_model=schemas.Material)
def read_material(material_id: int, db: Session = Depends(get_db)):
    material = db.query(Material).filter(Material.id == material_id).first()
    if material is None:
        raise HTTPException(status_code=404, detail="Material not found")
    return material

@app.put("/materials/{material_id}", response_model=schemas.Material)
def update_material(material_id: int, material: schemas.MaterialCreate, db: Session = Depends(get_db)):
    db_material = db.query(Material).filter(Material.id == material_id).first()
    if db_material is None:
        raise HTTPException(status_code=404, detail="Material not found")
    
    for key, value in material.dict().items():
        setattr(db_material, key, value)
    
    db.commit()
    db.refresh(db_material)
    return db_material

@app.delete("/materials/{material_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_material(material_id: int, db: Session = Depends(get_db)):
    db_material = db.query(Material).filter(Material.id == material_id).first()
    if db_material is None:
        raise HTTPException(status_code=404, detail="Material not found")
    
    db.delete(db_material)
    db.commit()
    return None

# Order CRUD Operations
@app.post("/orders/", response_model=schemas.Order, status_code=status.HTTP_201_CREATED)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    db_order = Order(
        order_date=order.order_date,
        status=order.status,
        customer_name=order.customer_name
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

@app.get("/orders/", response_model=List[schemas.Order])
def read_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    orders = db.query(Order).offset(skip).limit(limit).all()
    return orders

@app.get("/orders/{order_id}", response_model=schemas.Order)
def read_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@app.put("/orders/{order_id}", response_model=schemas.Order)
def update_order(order_id: int, order: schemas.OrderCreate, db: Session = Depends(get_db)):
    db_order = db.query(Order).filter(Order.id == order_id).first()
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    
    for key, value in order.dict().items():
        setattr(db_order, key, value)
    
    db.commit()
    db.refresh(db_order)
    return db_order

@app.delete("/orders/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(order_id: int, db: Session = Depends(get_db)):
    db_order = db.query(Order).filter(Order.id == order_id).first()
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    
    db.delete(db_order)
    db.commit()
    return None

# PlantProduct operations
@app.post("/plant-products/", status_code=status.HTTP_201_CREATED)
def create_plant_product(plant_product: PlantProductCreate, db: Session = Depends(get_db)):
    db_plant_product = PlantProduct(
        plant_id=plant_product.plant_id,
        product_id=plant_product.product_id,
        quantity=plant_product.quantity
    )
    db.add(db_plant_product)
    db.commit()
    db.refresh(db_plant_product)
    return db_plant_product

@app.get("/plant-products/")
def read_plant_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    plant_products = db.query(PlantProduct).offset(skip).limit(limit).all()
    return plant_products

@app.delete("/plant-products/{plant_product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_plant_product(plant_product_id: int, db: Session = Depends(get_db)):
    db_plant_product = db.query(PlantProduct).filter(PlantProduct.id == plant_product_id).first()
    if db_plant_product is None:
        raise HTTPException(status_code=404, detail="Plant-Product association not found")
    
    db.delete(db_plant_product)
    db.commit()
    return None

# PlantMaterial operations
@app.post("/plant-materials/", status_code=status.HTTP_201_CREATED)
def create_plant_material(plant_material: PlantMaterialCreate, db: Session = Depends(get_db)):
    db_plant_material = PlantMaterial(
        plant_id=plant_material.plant_id,
        material_id=plant_material.material_id,
        quantity=plant_material.quantity
    )
    db.add(db_plant_material)
    db.commit()
    db.refresh(db_plant_material)
    return db_plant_material

@app.get("/plant-materials/")
def read_plant_materials(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    plant_materials = db.query(PlantMaterial).offset(skip).limit(limit).all()
    return plant_materials

@app.delete("/plant-materials/{plant_material_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_plant_material(plant_material_id: int, db: Session = Depends(get_db)):
    db_plant_material = db.query(PlantMaterial).filter(PlantMaterial.id == plant_material_id).first()
    if db_plant_material is None:
        raise HTTPException(status_code=404, detail="Plant-Material association not found")
    
    db.delete(db_plant_material)
    db.commit()
    return None

# ProductMaterial operations
@app.post("/product-materials/", status_code=status.HTTP_201_CREATED)
def create_product_material(product_material: ProductMaterialCreate, db: Session = Depends(get_db)):
    db_product_material = ProductMaterial(
        product_id=product_material.product_id,
        material_id=product_material.material_id,
        quantity=product_material.quantity
    )
    db.add(db_product_material)
    db.commit()
    db.refresh(db_product_material)
    return db_product_material

@app.get("/product-materials/")
def read_product_materials(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    product_materials = db.query(ProductMaterial).offset(skip).limit(limit).all()
    return product_materials

@app.delete("/product-materials/{product_material_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product_material(product_material_id: int, db: Session = Depends(get_db)):
    db_product_material = db.query(ProductMaterial).filter(ProductMaterial.id == product_material_id).first()
    if db_product_material is None:
        raise HTTPException(status_code=404, detail="Product-Material association not found")
    
    db.delete(db_product_material)
    db.commit()
    return None

# OrderProduct operations
@app.post("/order-products/", status_code=status.HTTP_201_CREATED)
def create_order_product(order_product: OrderProductCreate, db: Session = Depends(get_db)):
    db_order_product = OrderProduct(
        order_id=order_product.order_id,
        product_id=order_product.product_id,
        quantity=order_product.quantity
    )
    db.add(db_order_product)
    db.commit()
    db.refresh(db_order_product)
    return db_order_product

@app.get("/order-products/")
def read_order_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    order_products = db.query(OrderProduct).offset(skip).limit(limit).all()
    return order_products

@app.delete("/order-products/{order_product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order_product(order_product_id: int, db: Session = Depends(get_db)):
    db_order_product = db.query(OrderProduct).filter(OrderProduct.id == order_product_id).first()
    if db_order_product is None:
        raise HTTPException(status_code=404, detail="Order-Product association not found")
    
    db.delete(db_order_product)
    db.commit()
    return None

# StorageProduct operations
@app.post("/storage-products/", status_code=status.HTTP_201_CREATED)
def create_storage_product(storage_product: StorageProductCreate, db: Session = Depends(get_db)):
    db_storage_product = StorageProduct(
        product_id=storage_product.product_id,
        quantity=storage_product.quantity
    )
    db.add(db_storage_product)
    db.commit()
    db.refresh(db_storage_product)
    return db_storage_product

@app.get("/storage-products/")
def read_storage_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    storage_products = db.query(StorageProduct).offset(skip).limit(limit).all()
    return storage_products

@app.put("/storage-products/{storage_product_id}")
def update_storage_product(storage_product_id: int, storage_product: StorageProductCreate, db: Session = Depends(get_db)):
    db_storage_product = db.query(StorageProduct).filter(StorageProduct.id == storage_product_id).first()
    if db_storage_product is None:
        raise HTTPException(status_code=404, detail="Storage Product not found")
    
    for key, value in storage_product.dict().items():
        setattr(db_storage_product, key, value)
    
    db.commit()
    db.refresh(db_storage_product)
    return db_storage_product

@app.delete("/storage-products/{storage_product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_storage_product(storage_product_id: int, db: Session = Depends(get_db)):
    db_storage_product = db.query(StorageProduct).filter(StorageProduct.id == storage_product_id).first()
    if db_storage_product is None:
        raise HTTPException(status_code=404, detail="Storage Product not found")
    
    db.delete(db_storage_product)
    db.commit()
    return None

# StorageMaterial operations
@app.post("/storage-materials/", status_code=status.HTTP_201_CREATED)
def create_storage_material(storage_material: StorageMaterialCreate, db: Session = Depends(get_db)):
    db_storage_material = StorageMaterial(
        material_id=storage_material.material_id,
        quantity=storage_material.quantity
    )
    db.add(db_storage_material)
    db.commit()
    db.refresh(db_storage_material)
    return db_storage_material

@app.get("/storage-materials/")
def read_storage_materials(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    storage_materials = db.query(StorageMaterial).offset(skip).limit(limit).all()
    return storage_materials

@app.put("/storage-materials/{storage_material_id}")
def update_storage_material(storage_material_id: int, storage_material: StorageMaterialCreate, db: Session = Depends(get_db)):
    db_storage_material = db.query(StorageMaterial).filter(StorageMaterial.id == storage_material_id).first()
    if db_storage_material is None:
        raise HTTPException(status_code=404, detail="Storage Material not found")
    
    for key, value in storage_material.dict().items():
        setattr(db_storage_material, key, value)
    
    db.commit()
    db.refresh(db_storage_material)
    return db_storage_material

@app.delete("/storage-materials/{storage_material_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_storage_material(storage_material_id: int, db: Session = Depends(get_db)):
    db_storage_material = db.query(StorageMaterial).filter(StorageMaterial.id == storage_material_id).first()
    if db_storage_material is None:
        raise HTTPException(status_code=404, detail="Storage Material not found")
    
    db.delete(db_storage_material)
    db.commit()
    return None

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

