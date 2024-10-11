from datetime import datetime
from typing import Annotated, Optional, List
from fastapi import APIRouter, Depends, HTTPException, status
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field

class CustomerResponse(BaseModel):
    customer_id: int
    name: str
    email: str
    total_spent: float
    loyalty_id: Optional[int]
    loyal_name: Optional[str]

class CustomerUpdateRequest(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None

class CustomerVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=6)