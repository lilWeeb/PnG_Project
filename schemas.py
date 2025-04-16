import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import Column, Integer, DECIMAL, String, ForeignKey, DateTime
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from decimal import Decimal

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_FILE = os.path.join(BASE_DIR, "project.db")
DATABASE_URL = "sqlite:///" + DATABASE_FILE
engine = create_engine(DATABASE_URL, echo=True)
Base = declarative_base()


try:
    with engine.connect() as connection:
        print("Database connected successfully!")
except Exception as e:
    print(f"Error connecting to database: {e}")

Session = sessionmaker(bind=engine)
session = Session()


# Base models (for creating items - they don't have IDs yet)
# class PlantBase(BaseModel):
#     name: str
#     location: Optional[str] = None
#     capacity: Optional[int] = None

# class ProductBase(BaseModel):
#     name: str
#     description: Optional[str] = None
#     category: Optional[str] = None
#     price: Optional[Decimal] = None

# class MaterialBase(BaseModel):
#     name: str
#     description: Optional[str] = None
#     unit: Optional[str] = None
#     cost: Optional[Decimal] = None

# class PlantProductBase(BaseModel):
#     plant_id: int
#     product_id: int
#     quantity: Optional[int] = None

# class PlantMaterialBase(BaseModel):
#     plant_id: int
#     material_id: int
#     quantity: Optional[int] = None

# class StorageProductBase(BaseModel):
#     product_id: int
#     quantity: int

# class StorageMaterialBase(BaseModel):
#     material_id: int
#     quantity: int

# class OrderBase(BaseModel):
#     order_date: datetime
#     status: str
#     customer_name: Optional[str] = None

# class ProductMaterialBase(BaseModel):
#     product_id: int
#     material_id: int
#     quantity: int

# class OrderProductBase(BaseModel):
#     order_id: int
#     product_id: int
#     quantity: int

# # Create models (for returning created items with IDs)
# class Plant(PlantBase):
#     id: int
#     name: str
#     location: Optional[str] = None
#     capacity: Optional[int] = None
#     # class Config:
#     #     orm_mode = True

# class Product(ProductBase):
#     id: int

#     class Config:
#         orm_mode = True

# class Material(MaterialBase):
#     id: int

#     class Config:
#         orm_mode = True

# class PlantProduct(PlantProductBase):
#     id: int

#     class Config:
#         orm_mode = True

# class PlantMaterial(PlantMaterialBase):
#     id: int

#     class Config:
#         orm_mode = True

# class StorageProduct(StorageProductBase):
#     id: int

#     class Config:
#         orm_mode = True

# class StorageMaterial(StorageMaterialBase):
#     id: int

#     class Config:
#         orm_mode = True

# class Order(OrderBase):
#     id: int

#     class Config:
#         orm_mode = True

# class ProductMaterial(ProductMaterialBase):
#     id: int

#     class Config:
#         orm_mode = True

# class OrderProduct(OrderProductBase):
#     id: int

#     class Config:
#         orm_mode = True

# # Update models (for partial updates)
# class PlantUpdate(BaseModel):
#     name: Optional[str] = None
#     location: Optional[str] = None
#     capacity: Optional[int] = None

# class ProductUpdate(BaseModel):
#     name: Optional[str] = None
#     description: Optional[str] = None
#     category: Optional[str] = None
#     price: Optional[Decimal] = None

# class MaterialUpdate(BaseModel):
#     name: Optional[str] = None
#     description: Optional[str] = None
#     unit: Optional[str] = None
#     cost: Optional[Decimal] = None

# class PlantProductUpdate(BaseModel):
#     plant_id: Optional[int] = None
#     product_id: Optional[int] = None
#     quantity: Optional[int] = None

# class PlantMaterialUpdate(BaseModel):
#     plant_id: Optional[int] = None
#     material_id: Optional[int] = None
#     quantity: Optional[int] = None

# class StorageProductUpdate(BaseModel):
#     product_id: Optional[int] = None
#     quantity: Optional[int] = None

# class StorageMaterialUpdate(BaseModel):
#     material_id: Optional[int] = None
#     quantity: Optional[int] = None

# class OrderUpdate(BaseModel):
#     order_date: Optional[datetime] = None
#     status: Optional[str] = None
#     customer_name: Optional[str] = None

# class ProductMaterialUpdate(BaseModel):
#     product_id: Optional[int] = None
#     material_id: Optional[int] = None
#     quantity: Optional[int] = None

# class OrderProductUpdate(BaseModel):
#     order_id: Optional[int] = None
#     product_id: Optional[int] = None
#     quantity: Optional[int] = None

class PlantBase(BaseModel):
    name: str
    location: Optional[str] = None
    capacity: Optional[int] = None

class PlantCreate(PlantBase):
    pass

class Plant(PlantBase):
    id: int
    class Config:
        orm_mode = True


class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = None

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int
    class Config:
        orm_mode = True


class MaterialBase(BaseModel):
    name: str
    description: Optional[str] = None
    unit: Optional[str] = None
    cost: Optional[float] = None

class MaterialCreate(MaterialBase):
    pass

class Material(MaterialBase):
    id: int
    class Config:
        orm_mode = True


class OrderBase(BaseModel):
    order_date: datetime
    status: str
    customer_name: Optional[str] = None

class OrderCreate(OrderBase):
    pass

class Order(OrderBase):
    id: int
    class Config:
        orm_mode = True