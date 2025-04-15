from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import Column, Integer, String, Decimal, ForeignKey, DateTime

DATABASE_URL = 'sqlite:///C:\Users\alexa\Desktop\Facultate\Sem2\Practica\Proiect\PnG_Project'
engine = create_engine(DATABASE_URL, echo=True)
Base = declarative_base()


try:
    with engine.connect() as connection:
        print("Database connected successfully!")
except Exception as e:
    print(f"Error connecting to database: {e}")

Session = sessionmaker(bind=engine)
session = Session()


class Plant(Base):
    __tablename__ = 'plant'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    location = Column(String)
    capacity = Column(Integer)
    plant_products = relationship("Plant_Products", back_populates="plant")
    plant_material = relationship("Plant_Material", back_populates="plant")

class Products(Base):
    __tablename__ = 'product'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String)
    category = Column(String)
    price = Column(Decimal(10, 2))
    plant_products = relationship("PlantProduct", back_populates="product")
    product_material = relationship("ProductMaterial", back_populates="product")
    storage_product = relationship("StorageProduct", back_populates="product")
    order_product = relationship("OrderProduct", back_populates="product")
    
class Plant_Product(Base):
    __tablename__ = 'plant_product'

    id = Column(Integer, primary_key=True, autoincrement=True)
    plant_id = Column(Integer, ForeignKey('plant.id'))
    product_id= Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer)
    products = relationship("Products", back_populates="plant_product")
    plant = relationship("Plant", back_populates="plant_product")

class Material(Base):
    __tablename__ = 'material'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String)
    unit = Column(String)
    cost = Column(Decimal(10, 2))
    plant_materials = relationship("PlantMaterial", back_populates="material")
    product_materials = relationship("ProductMaterial", back_populates="material")
    storage_material = relationship("StorageMaterial", back_populates="material")


class StorageMaterial(Base):
    __tablename__ = 'storage_material'

    id = Column(Integer, primary_key=True, autoincrement=True)
    material_id = Column(Integer, ForeignKey('material.id'))
    quantity = Column(Integer, nullable=False)
    material=relationship("Material", back_populates="storage_material")

class PlantMaterial(Base):
    __tablename__ = 'plant_material'

    id = Column(Integer, primary_key=True, autoincrement=True)
    plant_id = Column(Integer, ForeignKey('plant.id'))
    material_id = Column(Integer, ForeignKey('material.id'))
    quantity = Column(Decimal(10, 2))
    plant = relationship("Plant", back_populates="plant_materials")
    material = relationship("Material", back_populates="plant_material")

class Order(Base):
    __tablename__ = 'order'

    id = Column(Integer, primary_key=True, autoincrement=True)
    order_date = Column(DateTime, nullable=False)
    delivery_date = Column(DateTime, nullable=False)
    status = Column(String, nullable=False)
    order_product = relationship("OrderProduct", back_populates="order")
    

class ProductMaterial(Base):
    __tablename__ = 'product_material'

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey('product.id'))
    material_id = Column(Integer, ForeignKey('material.id'))
    quantity = Column(Integer, nullable=False)
    product = relationship("Products", back_populates="product_material")
    material = relationship("Material", back_populates="product_material")


class OrderProduct(Base):
    __tablename__ = 'order_product'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('order.id'))
    product_id = Column(Integer, ForeignKey('product.id'))
    quantity = Column(Integer, nullable=False)
    order = relationship("Order", back_populates="order_product")
    product = relationship("Products", back_populates="order_product")

class StorageProduct(Base):
    __tablename__ = 'storage_product'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey('product.id'))
    quantity = Column(Integer, nullable=False)
    product = relationship("Products", back_populates="storage_product")

