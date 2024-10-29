Backend Development Intern Project (The Coffeeshop System)

API Development: Developed and maintained RESTful API endpoints using FastAPI for The Coffeeshop system. Key functionalities include:

Authentication:

POST /auth/register: User registration

POST /auth/login: User login with JWT-based authentication

Order Management:

GET /orders/: Retrieve all orders

POST /orders/: Create a new order

GET /orders/{order_id}: Retrieve order details by ID

PUT /orders/{order_id}: Update an order by ID

DELETE /orders/{order_id}: Delete an order by ID

Customer Management:

GET /customers/: Retrieve customer details

PUT /customers/: Update customer information

PUT /customers/password: Change customer password

Admin Features:

Product Management:

GET /admin/products: Retrieve all products

POST /admin/products: Add a new product

GET /admin/products/{product_id}: Retrieve product details by ID

PUT /admin/products/{product_id}: Update product by ID

DELETE /admin/products/{product_id}: Delete product by ID

Customer & Order Management:

GET /admin/customers: Retrieve all customers

GET /admin/orders: Retrieve all orders

Revenue Reporting:

GET /revenue/statistics/daily: Daily revenue statistics

GET /revenue/statistics/monthly: Monthly revenue statistics

GET /revenue/statistics/yearly: Yearly revenue statistics

Technologies: FastAPI, SQLAlchemy, MySQL, JWT for authentication

Steps to Run The Coffeeshop API Project

Clone the Repository:

git clone <repository_url>
cd <repository_name>

Create a Virtual Environment and Install Dependencies:

python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
pip install -r requirements.txt

Set Up the Database:

Ensure you have MySQL installed and running.
Create a database for the project:

CREATE DATABASE coffeeshop;

Update the database connection details in the environment file (.env or config file) with your MySQL username, password, and database name.

Run Database Migrations (if applicable):

alembic upgrade head

Start the API Server:

uvicorn main:app --reload

Access the API Documentation:

Open http://127.0.0.1:8000/docs in your browser to view interactive API documentation.
