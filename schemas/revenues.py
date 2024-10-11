from datetime import datetime
from typing import Annotated, Optional, List
from fastapi import APIRouter, Depends, HTTPException, status
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field

class DailyRevenueResponse(BaseModel):
    date: datetime
    total_revenue: float

class MonthlyRevenueResponse(BaseModel):
    year: int
    month: int
    total_revenue: float

class YearlyRevenueResponse(BaseModel):
    year: int
    total_revenue: float
