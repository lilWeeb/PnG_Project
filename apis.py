from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from schemas import (
    Plant as Plant2, PlantCreate,
    Product, ProductCreate,
    Material, MaterialCreate,
    Order, OrderCreate

)
from database import get_db

app = FastAPI(title="Manufacturing Management API")

# Plant endpoints

@app.post("/plants/", response_model=Plant2)
def create_plant(plant: PlantCreate, db: Session = Depends(get_db)):
    db_plant = Plant2(**plant.dict())
    db.add(db_plant)
    db.commit()
    db.refresh(db_plant)
    return db_plant

@app.get("/plants/", response_model=List[Plant2])
def get_plants(db: Session = Depends(get_db)):
    return db.query(Plant2).all()

@app.get("/plants/{plant_id}", response_model=Plant2)
def get_plant(plant_id: int, db: Session = Depends(get_db)):
    plant = db.query(Plant2).get(plant_id)
    if not plant:
        raise HTTPException(status_code=404, detail="Plant not found")
    return plant

@app.delete("/plants/{plant_id}")
def delete_plant(plant_id: int, db: Session = Depends(get_db)):
    plant = db.query(Plant2).get(plant_id)
    if not plant:
        raise HTTPException(status_code=404, detail="Plant not found")
    db.delete(plant)
    db.commit()
    return {"detail": "Plant deleted successfully"}


# PRODUCT APIs
@app.post("/products/", response_model=Product)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@app.get("/products/", response_model=List[Product])
def get_products(db: Session = Depends(get_db)):
    return db.query(Product).all()


# MATERIAL APIs
@app.post("/materials/", response_model=Material)
def create_material(material: MaterialCreate, db: Session = Depends(get_db)):
    db_material = Material(**material.dict())
    db.add(db_material)
    db.commit()
    db.refresh(db_material)
    return db_material

@app.get("/materials/", response_model=List[Material])
def get_materials(db: Session = Depends(get_db)):
    return db.query(Material).all()


# ORDER APIs
@app.post("/orders/", response_model=Order)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    db_order = Order(**order.dict())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

@app.get("/orders/", response_model=List[Order])
def get_orders(db: Session = Depends(get_db)):
    return db.query(Order).all()