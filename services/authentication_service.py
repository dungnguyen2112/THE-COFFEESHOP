import os
from datetime import timedelta, datetime
from passlib.context import CryptContext
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from fastapi import HTTPException

from config.auth import create_access_token, pwd_context, ACCESS_TOKEN_EXPIRE_MINUTES
from models.customers import Customer
from schemas.auth import CustomerRequest, Token

def get_authen_service():
    try:
        auth_service = AuthenticationService()
        yield auth_service
    finally:
        pass

class AuthenticationService:
    def authenticate_customer(self, db: Session, email: str, password: str):
        print(f"Attempting to authenticate customer with email: {email}")
        customer = db.query(Customer).filter(Customer.email == email).first()
        if not customer:
            print("Customer not found.")
        elif not pwd_context.verify(password, customer.hashed_password):
            print("Password mismatch.")
        else:
            print("Customer authenticated successfully.")

        if not customer or not pwd_context.verify(password, customer.hashed_password):
            return None

        access_token = create_access_token(
            email=email,
            customer_id=customer.customer_id,
            role_id=customer.role_id,
            expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        return {"access_token": access_token, "token_type": "bearer"}

    def register_customer(self, db: Session, create_customer_request: CustomerRequest):
        """Register a new customer."""
        try:
            existing_customer = db.query(Customer).filter(Customer.email == create_customer_request.email).first()
            if existing_customer:
                raise HTTPException(status_code=400, detail="Email already registered")

            hashed_password = pwd_context.hash(create_customer_request.password)

            new_customer = Customer(
                name=create_customer_request.name,
                email=create_customer_request.email,
                hashed_password=hashed_password,
                phone_number=create_customer_request.phone_number,
                address=create_customer_request.address,
                role_id=create_customer_request.role_id
            )

            db.add(new_customer)
            db.commit()
            db.refresh(new_customer)

            return {"message": "Customer created successfully"}

        except HTTPException as e:
            db.rollback()
            raise e

        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")



