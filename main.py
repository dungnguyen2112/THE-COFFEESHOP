from fastapi import FastAPI
from routers.auth import router as auth_router
from routers.orders import router as order_router
from routers.customers import router as customer_router
from routers.admin import router as admin_router
from routers.revenuedate import router as revenue_router
from config.database import Base, engine
from models.customers import Customer  # Import models
from models.roles import Role          # Import Role model
from models.customer_loyalty import CustomerLoyalty  # Import other models if needed
from models.orders import Order
from models.order_items import OrderItem
from models.products import Product

# Ensure all models are imported before calling this line
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include your authentication router
app.include_router(auth_router)
app.include_router(order_router)
app.include_router(customer_router)
app.include_router(admin_router)
app.include_router(revenue_router)


@app.get("/")
def read_root():
    return {"message": "Welcome to the Flower Shop API meo meo"}
