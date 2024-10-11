from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from config.auth import get_current_customer
from config.database import get_db
from schemas.orders import OrderRequest, OrderResponse, OrderItemResponse, OrderUpdate
from services.order_service import OrderService
from schemas.base_response import BaseResponse

router = APIRouter(
    prefix='/orders',
    tags=['orders']
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=BaseResponse[OrderResponse])
def create_order(
    order: OrderRequest,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_customer)
):
    order_service = OrderService(db)
    try:
        new_order = order_service.create_order(order, user.customer_id)
        return BaseResponse(
            message="Order created successfully",
            status="success",
            data=OrderResponse(
                order_id=new_order.order_id,
                customer_id=new_order.customer_id,
                total_amount=new_order.total_amount,
                order_date=new_order.order_date,
                items=[OrderItemResponse(
                    order_item_id=item.order_item_id,
                    order_id=item.order_id,
                    product_id=item.product_id,
                    quantity=item.quantity,
                    price_at_purchase=item.price_at_purchase
                ) for item in new_order.items]
            )
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating order: " + str(e)
        )


@router.get("/{order_id}", status_code=status.HTTP_200_OK, response_model=BaseResponse[OrderResponse])
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_customer)
):
    order_service = OrderService(db)
    try:
        order = order_service.get_order(order_id, user.customer_id)
        return BaseResponse(
            message="Order retrieved successfully",
            status="success",
            data=OrderResponse(
                order_id=order.order_id,
                customer_id=order.customer_id,
                total_amount=order.total_amount,
                order_date=order.order_date,
                items=[OrderItemResponse(
                    order_item_id=item.order_item_id,
                    order_id=item.order_id,
                    product_id=item.product_id,
                    quantity=item.quantity,
                    price_at_purchase=item.price_at_purchase
                ) for item in order.items]
            )
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving order: " + str(e)
        )


@router.put("/{order_id}", response_model=BaseResponse[OrderResponse])
def update_order(
    order_id: int,
    order: OrderUpdate,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_customer)
):
    order_service = OrderService(db)
    try:
        updated_order = order_service.update_order(order_id, order, user.customer_id)
        return BaseResponse(
            message="Order updated successfully",
            status="success",
            data=OrderResponse(
                order_id=updated_order.order_id,
                customer_id=updated_order.customer_id,
                total_amount=updated_order.total_amount,
                order_date=updated_order.order_date,
                items=[OrderItemResponse(
                    order_item_id=item.order_item_id,
                    order_id=item.order_id,
                    product_id=item.product_id,
                    quantity=item.quantity,
                    price_at_purchase=item.price_at_purchase
                ) for item in updated_order.items]
            )
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating order: " + str(e)
        )


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(
    order_id: int,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_customer)
):
    order_service = OrderService(db)
    try:
        order_service.delete_order(order_id, user.customer_id)
        return BaseResponse(
            message="Order deleted successfully",
            status="success",
            data={}
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deleting order: " + str(e)
        )


@router.get("/", status_code=status.HTTP_200_OK, response_model=BaseResponse[List[OrderResponse]])
def get_all_orders(
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_customer)
):
    order_service = OrderService(db)
    try:
        orders = order_service.get_all_orders(user.customer_id)
        return BaseResponse(
            message="Orders retrieved successfully",
            status="success",
            data=[OrderResponse(
                order_id=order.order_id,
                customer_id=order.customer_id,
                total_amount=order.total_amount,
                order_date=order.order_date,
                items=[OrderItemResponse(
                    order_item_id=item.order_item_id,
                    order_id=item.order_id,
                    product_id=item.product_id,
                    quantity=item.quantity,
                    price_at_purchase=item.price_at_purchase
                ) for item in order.items]
            ) for order in orders]
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving orders: " + str(e)
        )
