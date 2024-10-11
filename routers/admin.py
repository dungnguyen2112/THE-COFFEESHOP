from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel

from models.customers import Customer
from schemas.customers import CustomerResponse
from schemas.orders import OrderResponse
from schemas.products import ProductRequest, ProductResponse, ProductUpdateRequest
from services.admin_service import AdminService
from config.auth import get_current_customer
from config.database import get_db
from schemas.base_response import BaseResponse

router = APIRouter(
    prefix='/admin',
    tags=['admin']
)

def admin_required(current_user: Customer):
    if current_user.role_id != 1:
        raise HTTPException(status_code=403, detail="You do not have sufficient permissions")

@router.post("/products", status_code=status.HTTP_201_CREATED, response_model=BaseResponse[ProductResponse])
async def create_product(
    product: ProductRequest,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_customer)
):
    admin_required(current_user)
    service = AdminService(db)
    try:
        created_product = service.create_product(product)
        return BaseResponse(message="Product created successfully", status="success", data=created_product)
    except ValueError as e:
        return BaseResponse(message=str(e), status="error", data={})
    except Exception as e:
        print(f"Unexpected error during product creation: {e}")
        return BaseResponse(message="Internal Server Error", status="error", data={})

@router.get("/products/{product_id}", status_code=status.HTTP_200_OK, response_model=BaseResponse[ProductResponse])
async def get_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_customer)
):
    admin_required(current_user)
    service = AdminService(db)
    try:
        product = service.get_product(product_id)
        return BaseResponse(message="Product retrieved successfully", status="success", data=product)
    except ValueError as e:
        return BaseResponse(message=str(e), status="error", data={})
    except Exception as e:
        print(f"Unexpected error during product retrieval: {e}")
        return BaseResponse(message="Internal Server Error", status="error", data={})

@router.put("/products/{product_id}", status_code=status.HTTP_200_OK, response_model=BaseResponse[ProductResponse])
async def update_product(
    product_id: int,
    product: ProductUpdateRequest,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_customer)
):
    admin_required(current_user)
    service = AdminService(db)
    try:
        updated_product = service.update_product(product_id, product)
        return BaseResponse(message="Product updated successfully", status="success", data=updated_product)
    except ValueError as e:
        return BaseResponse(message=str(e), status="error", data={})
    except Exception as e:
        print(f"Unexpected error during product update: {e}")
        return BaseResponse(message="Internal Server Error", status="error", data={})

@router.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_customer)
):
    admin_required(current_user)
    service = AdminService(db)
    try:
        service.delete_product(product_id)
        return BaseResponse(message="Product deleted successfully", status="success", data={})
    except ValueError as e:
        return BaseResponse(message=str(e), status="error", data={})
    except Exception as e:
        print(f"Unexpected error during product deletion: {e}")
        return BaseResponse(message="Internal Server Error", status="error", data={})

@router.get("/products", status_code=status.HTTP_200_OK, response_model=BaseResponse[List[ProductResponse]])
async def get_all_products(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_customer)
):
    admin_required(current_user)
    service = AdminService(db)
    try:
        products = service.get_all_products()
        return BaseResponse(message="Products retrieved successfully", status="success", data=products)
    except Exception as e:
        print(f"Unexpected error during retrieval of all products: {e}")
        return BaseResponse(message="Internal Server Error", status="error", data=[])

@router.get("/customers", status_code=status.HTTP_200_OK, response_model=BaseResponse[List[CustomerResponse]])
async def get_all_customers(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_customer)
):
    admin_required(current_user)
    service = AdminService(db)
    try:
        customers = service.get_all_customers()
        return BaseResponse(message="Customers retrieved successfully", status="success", data=customers)
    except Exception as e:
        print(f"Unexpected error during retrieval of all customers: {e}")
        return BaseResponse(message="Internal Server Error", status="error", data=[])

@router.get("/orders", status_code=status.HTTP_200_OK, response_model=BaseResponse[List[OrderResponse]])
async def get_all_orders(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_customer)
):
    admin_required(current_user)
    service = AdminService(db)
    try:
        orders = service.get_all_orders()
        return BaseResponse(message="Orders retrieved successfully", status="success", data=orders)
    except Exception as e:
        print(f"Unexpected error during retrieval of all orders: {e}")
        return BaseResponse(message="Internal Server Error", status="error", data=[])
