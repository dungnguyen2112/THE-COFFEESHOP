from typing import List, Optional
from sqlalchemy.orm import Session

from models.customer_loyalty import CustomerLoyalty
from models.customers import Customer
from models.orders import Order
from models.products import Product
from schemas.customers import CustomerResponse
from schemas.orders import OrderResponse
from schemas.products import ProductRequest, ProductResponse, ProductUpdateRequest


class AdminService:
    def __init__(self, db: Session):
        self.db = db

    def create_product(self, product: ProductRequest) -> ProductResponse:
        db_product = Product(**product.dict())
        try:
            self.db.add(db_product)
            self.db.commit()
            self.db.refresh(db_product)
            return db_product
        except Exception as e:
            self.db.rollback()
            raise ValueError(f"Error creating product: {str(e)}")

    def get_product(self, product_id: int) -> ProductResponse:
        db_product = self.db.query(Product).filter(Product.product_id == product_id).first()
        if db_product is None:
            raise ValueError("Product not found")
        return db_product

    def update_product(self, product_id: int, product_update: ProductUpdateRequest) -> ProductResponse:
        db_product = self.db.query(Product).filter(Product.product_id == product_id).first()
        if db_product is None:
            raise ValueError("Product not found")

        for key, value in product_update.dict().items():
            if value is not None:
                setattr(db_product, key, value)

        self.db.commit()
        self.db.refresh(db_product)
        return db_product

    def delete_product(self, product_id: int):
        db_product = self.db.query(Product).filter(Product.product_id == product_id).first()
        if db_product is None:
            raise ValueError("Product not found")
        self.db.delete(db_product)
        self.db.commit()

    def get_all_products(self) -> List[ProductResponse]:
        return self.db.query(Product).all()

    def get_all_customers(self) -> List[CustomerResponse]:
        customers = self.db.query(Customer).all()
        customer_responses = []

        for customer in customers:
            loyal_name = None
            if customer.loyalty_id:
                loyalty = self.db.query(CustomerLoyalty).filter(CustomerLoyalty.loyalty_id == customer.loyalty_id).first()
                if loyalty:
                    loyal_name = loyalty.status

            customer_responses.append(CustomerResponse(
                customer_id=customer.customer_id,
                name=customer.name,
                email=customer.email,
                total_spent=customer.total_spent,
                loyalty_id=customer.loyalty_id,
                loyal_name=loyal_name
            ))

        return customer_responses

    def get_all_orders(self) -> List[OrderResponse]:
        return self.db.query(Order).all()
