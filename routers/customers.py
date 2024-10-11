from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from models.customers import Customer
from schemas.customers import CustomerResponse, CustomerUpdateRequest, CustomerVerification
from services.customer_service import CustomerService
from config.auth import get_current_customer
from config.database import get_db
from schemas.base_response import BaseResponse

router = APIRouter(
    prefix='/customers',
    tags=['customers']
)

db_dependency = Annotated[Session, Depends(get_db)]
customer_dependency = Annotated[Customer, Depends(get_current_customer)]

@router.get('/', response_model=BaseResponse[CustomerResponse], status_code=status.HTTP_200_OK)
async def get_customer(
        customer: customer_dependency,
        db: db_dependency
):
    if customer is None:
        return BaseResponse(message='Authentication Failed', status='error', data={})

    service = CustomerService(db)
    try:
        customer_data = service.get_customer(customer.customer_id)
        return BaseResponse(message='Customer retrieved successfully', status='success', data=customer_data)
    except ValueError as e:
        return BaseResponse(message=str(e), status='error', data={})
    except Exception as e:
        return BaseResponse(message='Internal Server Error', status='error', data={})

@router.put('/', response_model=BaseResponse[CustomerResponse], status_code=status.HTTP_200_OK)
async def update_customer(
        customer: customer_dependency,
        customer_update: CustomerUpdateRequest,
        db: db_dependency
):
    if customer is None:
        return BaseResponse(message='Authentication Failed', status='error', data={})

    service = CustomerService(db)
    try:
        updated_customer = service.update_customer(customer.customer_id, customer_update)
        return BaseResponse(message='Customer updated successfully', status='success', data=updated_customer)
    except ValueError as e:
        return BaseResponse(message=str(e), status='error', data={})
    except Exception as e:
        return BaseResponse(message='Internal Server Error', status='error', data={})

@router.put("/password", response_model=BaseResponse[dict], status_code=status.HTTP_200_OK)
async def change_password(
        customer: customer_dependency,
        db: db_dependency,
        verification: CustomerVerification
):
    if customer is None:
        return BaseResponse(message='Authentication Failed', status='error', data={})

    service = CustomerService(db)
    try:
        service.change_password(customer.customer_id, verification)
        return BaseResponse(message='Password updated successfully', status='success', data={})
    except ValueError as e:
        return BaseResponse(message=str(e), status='error', data={})
    except Exception as e:
        return BaseResponse(message='Internal Server Error', status='error', data={})
