from typing import Optional
from datetime import date
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from schemas.revenues import DailyRevenueResponse, MonthlyRevenueResponse, YearlyRevenueResponse
from schemas.base_response import BaseResponse
from services.revenue_service import RevenueService
from config.auth import get_current_customer
from config.database import get_db

router = APIRouter(
    prefix='/revenue',
    tags=['revenue']
)

db_dependency = Depends(get_db)
customer_dependency = Depends(get_current_customer)

def admin_required(current_user: dict):
    if current_user.role_id != 1:
        raise HTTPException(status_code=403, detail="You do not have sufficient permissions")

@router.get("/statistics/daily", response_model=BaseResponse[DailyRevenueResponse])
def get_daily_revenue(
    date: Optional[date] = Query(None),
    db: Session = db_dependency,
    current_user: dict = customer_dependency
):
    admin_required(current_user)
    service = RevenueService(db)
    try:
        daily_revenue = service.get_daily_revenue(date)
        return BaseResponse(
            message="Daily revenue statistics retrieved successfully",
            status="success",
            data=daily_revenue
        )
    except Exception as e:
        return BaseResponse(
            message=f"Error retrieving daily revenue: {str(e)}",
            status="error",
            data={}
        )

@router.get("/statistics/monthly", response_model=BaseResponse[MonthlyRevenueResponse])
def get_monthly_revenue(
    year: Optional[int] = Query(None),
    month: Optional[int] = Query(None),
    db: Session = db_dependency,
    current_user: dict = customer_dependency
):
    admin_required(current_user)
    service = RevenueService(db)
    try:
        monthly_revenue = service.get_monthly_revenue(year, month)
        return BaseResponse(
            message="Monthly revenue statistics retrieved successfully",
            status="success",
            data=monthly_revenue
        )
    except Exception as e:
        return BaseResponse(
            message=f"Error retrieving monthly revenue: {str(e)}",
            status="error",
            data={}
        )

@router.get("/statistics/yearly", response_model=BaseResponse[YearlyRevenueResponse])
def get_yearly_revenue(
    year: Optional[int] = Query(None),
    db: Session = db_dependency,
    current_user: dict = customer_dependency
):
    admin_required(current_user)
    service = RevenueService(db)
    try:
        yearly_revenue = service.get_yearly_revenue(year)
        return BaseResponse(
            message="Yearly revenue statistics retrieved successfully",
            status="success",
            data=yearly_revenue
        )
    except Exception as e:
        return BaseResponse(
            message=f"Error retrieving yearly revenue: {str(e)}",
            status="error",
            data={}
        )
