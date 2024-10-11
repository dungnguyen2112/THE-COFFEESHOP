from datetime import datetime
from typing import Annotated, Optional, List
from fastapi import APIRouter, Depends, HTTPException, status
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field

class ProductRequest(BaseModel):
    name: str = Field(..., min_length=1)
    description: Optional[str] = None
    price: float = Field(..., ge=0)
    stock_quantity: int = Field(..., ge=0)

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Rose Bouquet",
                "description": "A beautiful bouquet of red roses",
                "price": 29.99,
                "stock_quantity": 10
            }
        }

class ProductResponse(BaseModel):
    product_id: int
    name: str
    description: Optional[str]
    price: float
    stock_quantity: int

class ProductUpdateRequest(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    stock_quantity: Optional[int] = None
