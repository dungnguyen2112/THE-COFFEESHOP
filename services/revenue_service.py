from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from models.orders import Order
from schemas.revenues import DailyRevenueResponse, MonthlyRevenueResponse, YearlyRevenueResponse
from datetime import date

class RevenueService:
    def __init__(self, db: Session):
        self.db = db

    def get_daily_revenue(self, date: Optional[date]) -> DailyRevenueResponse:
        query = self.db.query(
            func.date(Order.order_date).label('date'),
            func.sum(Order.total_amount).label('total_revenue')
        )

        if date:
            query = query.filter(func.date(Order.order_date) == date)

        result = query.group_by(
            func.date(Order.order_date)
        ).first()

        if result is None:
            return DailyRevenueResponse(date=date, total_revenue=0.0)

        return DailyRevenueResponse(date=result.date, total_revenue=result.total_revenue)

    def get_monthly_revenue(self, year: Optional[int], month: Optional[int]) -> MonthlyRevenueResponse:
        query = self.db.query(
            func.extract('year', Order.order_date).label('year'),
            func.extract('month', Order.order_date).label('month'),
            func.sum(Order.total_amount).label('total_revenue')
        )

        if year:
            query = query.filter(func.extract('year', Order.order_date) == year)
        if month:
            query = query.filter(func.extract('month', Order.order_date) == month)

        result = query.group_by(
            func.extract('year', Order.order_date),
            func.extract('month', Order.order_date)
        ).first()

        if result is None:
            return MonthlyRevenueResponse(year=year or 0, month=month or 0, total_revenue=0.0)

        return MonthlyRevenueResponse(year=int(result.year), month=int(result.month), total_revenue=result.total_revenue)

    def get_yearly_revenue(self, year: Optional[int]) -> YearlyRevenueResponse:
        query = self.db.query(
            func.extract('year', Order.order_date).label('year'),
            func.sum(Order.total_amount).label('total_revenue')
        )

        if year:
            query = query.filter(func.extract('year', Order.order_date) == year)

        result = query.group_by(
            func.extract('year', Order.order_date)
        ).first()

        if result is None:
            return YearlyRevenueResponse(year=year or 0, total_revenue=0.0)

        return YearlyRevenueResponse(year=int(result.year), total_revenue=result.total_revenue)
