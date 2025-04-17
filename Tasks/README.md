Project Statement: Plant Management System Development

Objective:
Split into teams of 3 members.
Your task is to develop a Plant Management System that models the operations of a manufacturing plant. This system will track various entities such as plants, products, materials, orders, and their relationships.
By the end of this project, you will create a set of SQLAlchemy ORM classes and FastAPI endpoints to handle CRUD operations for these entities, along with tests and GitHub actions.

Background:
In a manufacturing plant, various processes are involved in producing goods. You will model the following entities and their relationships:

    Plant: Represents a manufacturing facility where products are produced.
    Product: Represents the items manufactured by the plant, including their details such as name, description, category, and price.
    Material: Represents the raw materials or components used to manufacture products.
    Order: Represents customer orders for products, including details such as order date, customer name, and status.
    Storage: Represents storage for materials and storage for products
    Relationships: Define relationships between plants and products, products and materials, and orders and products to ensure the system accurately reflects the real-world interactions.

Requirements:
Part 1: Class Design
Identify Entities:
Based on the description above, identify the main entities involved in the processes of a plant.

    Define SQLAlchemy Classes:
        For each identified entity, create a SQLAlchemy ORM class with the following attributes:
            Plant:
                id: Integer (Primary Key)
                name: String (Unique)
                location: String
                capacity: Integer
            Product:
                id: Integer (Primary Key)
                name: String (Unique)
                description: String (Optional)
                category: String (Optional)
                price: Decimal
            Material:
                id: Integer (Primary Key)
                name: String (Unique)
                description: String (Optional)
                unit: String (Optional)
                cost: Decimal
            Order:
                id: Integer (Primary Key)
                order_date: DateTime
                customer_name: String
                status: String
            PlantProduct (Many-to-Many Relationship):
                id: Integer (Primary Key)
                plant_id: Integer (Foreign Key referencing Plant)
                product_id: Integer (Foreign Key referencing Product)
                quantity: Decimal
            ProductMaterial (Many-to-Many Relationship):
                id: Integer (Primary Key)
                product_id: Integer (Foreign Key referencing Product)
                material_id: Integer (Foreign Key referencing Material)
                quantity: Decimal
            PlantMaterial (Many-to-Many Relationship):
                id: Integer (Primary Key)
                plant_id: Integer (Foreign Key referencing Plant)
                material_id: Integer (Foreign Key referencing Material)
                quantity: Decimal
            OrderProduct (Many-to-Many Relationship):
                id: Integer (Primary Key)
                order_id: Integer (Foreign Key referencing Order)
                product_id: Integer (Foreign Key referencing Product)
                quantity: Integer
            StorageProduct (One-to-Many Relationship)
                id: Integer (Primary key)
                product_id: Integer (ForeignKey referencing Products)
                quantity: Integer
            StorageMaterial (One-to-Many Relationship)
                id: Integer (Primary key)
                material_id: Integer (ForeignKey referencing Materials)
                quantity: Integer

Part 2: API Development
Create FastAPI Endpoints:
For each entity, create FastAPI endpoints to perform CRUD operations:
For example, Plant Endpoints:
POST /plants/: Create a new plant.
GET /plants/: Retrieve a list of all plants.
GET /plants/{id}: Retrieve a specific plant by ID.
PUT /plants/{id}: Update a specific plant.
DELETE /plants/{id}: Delete a specific plant.

    Implement Dependency Injection:
        Use FastAPI’s dependency injection to manage database sessions.

Part 3: Testing and GitHub Actions
Testing:
Create unit tests using pytest for each endpoint to ensure they function correctly.

    Version control:
        Create a GitHub repository and use it for storing your code and working together.
        You can use multiple branches and merge your code parts.

    GitHub actions:
        Your tests should run automatically on push and pull_request

Deliverables:
Your Python code, should include:
SQLAlchemy ORM classes for each entity.
FastAPI endpoints for CRUD operations.
Unit tests for each endpoint.
GitHub storage and actions.
Bonus: Documentation explaining your design choices, how to set up the project, and how to test the API endpoints.

    Extra:
        Data Visualization of your choice
        Create logic for material consumption based on orders and products delivered

\*\*\* Note: ALL FILES HAVE TO BE IN THE SAME FOLDER NAMED PROJECT_TEAM#!!!
.
