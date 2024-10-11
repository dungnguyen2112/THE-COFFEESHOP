from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field

class OrderItemResponse(BaseModel):
    order_item_id: int
    order_id: int
    product_id: int
    quantity: int
    price_at_purchase: float

class OrderItemRequest(BaseModel):
    product_id: int = Field(..., ge=1)
    quantity: int = Field(..., ge=1)

class OrderRequest(BaseModel):
    order_date: Optional[datetime] = Field(default_factory=datetime.utcnow)
    items: List[OrderItemRequest]

    class Config:
        json_schema_extra = {
            "example": {
                "order_date": "2024-08-27T10:00:00Z",
                "items": [
                    {"product_id": 1, "quantity": 2},
                    {"product_id": 2, "quantity": 1}
                ]
            }
        }

class OrderResponse(BaseModel):
    order_id: int
    customer_id: int
    total_amount: float
    order_date: datetime
    items: List[OrderItemResponse]

    class Config:
        from_attributes = True

class OrderUpdate(BaseModel):
    order_date: Optional[datetime] = None
    items: Optional[List[OrderItemRequest]] = None

class ErrorResponse(BaseModel):
    message: str
    status: str
