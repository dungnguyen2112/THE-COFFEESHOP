from datetime import datetime
from typing import Annotated, Optional, List
from fastapi import APIRouter, Depends, HTTPException, status
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field

class CustomerRequest(BaseModel):
    name: str = Field(..., min_length=3)
    email: str = Field(..., min_length=3)
    password: str = Field(..., min_length=6)
    phone_number: str = Field(..., min_length=3)
    address: str = Field(..., min_length=3)
    role_id: int = Field(..., ge=1)

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Nguyễn Văn A",
                "email": "sacxc@gmail.com",
                "password": "123456",
                "phone_number": "0123456789",
                "address": "Hà Nội",
                "role_id": 1
            }
        }

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
    role_id: Optional[int] = None