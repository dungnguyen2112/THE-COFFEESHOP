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
