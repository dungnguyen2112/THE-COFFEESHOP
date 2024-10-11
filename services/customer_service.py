from sqlalchemy.orm import Session
from passlib.context import CryptContext
from models.customer_loyalty import CustomerLoyalty
from models.customers import Customer
from schemas.customers import CustomerUpdateRequest, CustomerVerification

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class CustomerService:
    def __init__(self, db: Session):
        self.db = db

    def get_customer(self, customer_id: int):
        customer_model = self.db.query(Customer).filter(Customer.customer_id == customer_id).first()
        if not customer_model:
            raise ValueError("Customer not found")

        loyal_name = None
        if customer_model.loyalty_id:
            loyalty_model = self.db.query(CustomerLoyalty).filter(
                CustomerLoyalty.loyalty_id == customer_model.loyalty_id).first()
            if loyalty_model:
                loyal_name = loyalty_model.status

        return {
            "customer_id": customer_model.customer_id,
            "name": customer_model.name,
            "email": customer_model.email,
            "address": customer_model.address,
            "total_spent": customer_model.total_spent,
            "loyalty_id": customer_model.loyalty_id,
            "loyal_name": loyal_name
        }

    def update_customer(self, customer_id: int, customer_update: CustomerUpdateRequest):
        customer_model = self.db.query(Customer).filter(Customer.customer_id == customer_id).first()
        if not customer_model:
            raise ValueError("Customer not found")

        if customer_update.name:
            customer_model.name = customer_update.name
        if customer_update.email:
            customer_model.email = customer_update.email
        if customer_update.phone_number:
            customer_model.phone_number = customer_update.phone_number
        if customer_update.address:
            customer_model.address = customer_update.address

        if customer_model.loyalty_id:
            loyalty_model = self.db.query(CustomerLoyalty).filter(
                CustomerLoyalty.loyalty_id == customer_model.loyalty_id).first()
            loyal_name = loyalty_model.status if loyalty_model else None

        try:
            self.db.add(customer_model)
            self.db.commit()
            return {
                "customer_id": customer_model.customer_id,
                "name": customer_model.name,
                "email": customer_model.email,
                "address": customer_model.address,
                "total_spent": customer_model.total_spent,
                "loyalty_id": customer_model.loyalty_id,
                "loyal_name": loyal_name
            }
        except Exception as e:
            self.db.rollback()
            raise e

    def change_password(self, customer_id: int, verification: CustomerVerification):
        customer_model = self.db.query(Customer).filter(Customer.customer_id == customer_id).first()
        if not customer_model:
            raise ValueError("Customer not found")

        if not bcrypt_context.verify(verification.password, customer_model.hashed_password):
            raise ValueError("Incorrect password")

        hashed_new_password = bcrypt_context.hash(verification.new_password)
        customer_model.hashed_password = hashed_new_password

        try:
            self.db.add(customer_model)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise e
