from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import datetime

from models.customers import Customer
from models.order_items import OrderItem
from models.orders import Order
from models.products import Product
from models.customer_loyalty import CustomerLoyalty
from schemas.orders import OrderRequest, OrderUpdate


class OrderService:
    def __init__(self, db: Session):
        self.db = db

    def determine_loyalty_id(self, total_spent: float) -> Optional[int]:
        loyalty = self.db.query(CustomerLoyalty).order_by(CustomerLoyalty.loyalty_points.desc()).all()
        for level in loyalty:
            if total_spent >= level.loyalty_points:
                return level.loyalty_id
        return None

    def create_order(self, order: OrderRequest, customer_id: int) -> Order:
        try:
            total_amount = 0
            order_items = []
            product_ids = [item.product_id for item in order.items]
            products = self.db.query(Product).filter(Product.product_id.in_(product_ids)).all()
            product_dict = {product.product_id: product for product in products}

            for item in order.items:
                product = product_dict.get(item.product_id)
                if not product:
                    raise ValueError(f"Product ID {item.product_id} not found")
                if product.stock_quantity < item.quantity:
                    raise ValueError(f"Not enough stock for product ID {item.product_id}")
                if product.stock_quantity < 0:
                    raise ValueError(f"Product ID {item.product_id} is out of stock")
                price_at_purchase = product.price
                total_amount += price_at_purchase * item.quantity
                order_items.append(OrderItem(
                    product_id=item.product_id,
                    quantity=item.quantity,
                    price_at_purchase=price_at_purchase
                ))

            db_order = Order(
                customer_id=customer_id,
                order_date=order.order_date,
                total_amount=total_amount
            )
            self.db.add(db_order)
            self.db.commit()
            self.db.refresh(db_order)

            for item in order_items:
                db_order_item = OrderItem(
                    order_id=db_order.order_id,
                    product_id=item.product_id,
                    quantity=item.quantity,
                    price_at_purchase=item.price_at_purchase
                )
                product = self.db.query(Product).filter(Product.product_id == item.product_id).first()
                product.stock_quantity -= item.quantity
                self.db.add(db_order_item)

            self.db.commit()
            self.db.refresh(db_order)

            db_customer = self.db.query(Customer).filter(Customer.customer_id == customer_id).first()
            db_customer.total_spent += total_amount
            new_loyalty_id = self.determine_loyalty_id(db_customer.total_spent)
            if new_loyalty_id:
                db_customer.loyalty_id = new_loyalty_id
            self.db.add(db_customer)
            self.db.commit()
            self.db.refresh(db_customer)

            return db_order

        except IntegrityError:
            self.db.rollback()
            raise ValueError("Invalid customer or product ID")
        except Exception as e:
            self.db.rollback()
            raise e

    def get_order(self, order_id: int, customer_id: int) -> Order:
        order = self.db.query(Order).filter(Order.order_id == order_id, Order.customer_id == customer_id).first()
        if order is None:
            raise ValueError("Order not found")
        return order

    def update_order(self, order_id: int, order_update: OrderUpdate, customer_id: int) -> Order:
        try:
            db_order = self.db.query(Order).filter(Order.order_id == order_id,
                                                   Order.customer_id == customer_id).first()
            if db_order is None:
                raise ValueError("Order not found")

            if order_update.order_date is not None:
                db_order.order_date = order_update.order_date

            if order_update.items is not None:
                existing_items = {item.product_id: item for item in db_order.items}
                new_total_amount = 0

                product_ids = [item.product_id for item in order_update.items]
                products = self.db.query(Product).filter(Product.product_id.in_(product_ids)).all()
                product_dict = {product.product_id: product for product in products}

                if len(product_dict) != len(product_ids):
                    missing_product_ids = set(product_ids) - set(product_dict.keys())
                    raise ValueError(f"Products with IDs {missing_product_ids} not found")

                for item in order_update.items:
                    product = product_dict[item.product_id]
                    price_at_purchase = product.price
                    new_total_amount += price_at_purchase * item.quantity

                    if item.product_id in existing_items:
                        existing_item = existing_items[item.product_id]
                        existing_item.quantity = item.quantity
                        existing_item.price_at_purchase = price_at_purchase
                    else:
                        db_order_item = OrderItem(
                            order_id=db_order.order_id,
                            product_id=item.product_id,
                            quantity=item.quantity,
                            price_at_purchase=price_at_purchase
                        )
                        self.db.add(db_order_item)

                item_ids_to_keep = {item.product_id for item in order_update.items}
                for existing_item in db_order.items:
                    if existing_item.product_id not in item_ids_to_keep:
                        self.db.delete(existing_item)

                db_customer = self.db.query(Customer).filter(Customer.customer_id == customer_id).first()
                db_customer.total_spent -= db_order.total_amount
                db_order.total_amount = new_total_amount
                db_customer.total_spent += new_total_amount
                new_loyalty_id = self.determine_loyalty_id(db_customer.total_spent)
                db_customer.loyalty_id = new_loyalty_id
                self.db.add(db_customer)

            self.db.commit()
            self.db.refresh(db_order)

            return db_order

        except IntegrityError as e:
            self.db.rollback()
            raise ValueError(f"Integrity error: {str(e)}")
        except Exception as e:
            self.db.rollback()
            raise e

    def delete_order(self, order_id: int, customer_id: int) -> None:
        db_order = self.db.query(Order).filter(Order.order_id == order_id, Order.customer_id == customer_id).first()
        if db_order is None:
            raise ValueError("Order not found")

        db_customer = self.db.query(Customer).filter(Customer.customer_id == customer_id).first()
        db_customer.total_spent -= db_order.total_amount
        new_loyalty_id = self.determine_loyalty_id(db_customer.total_spent)
        db_customer.loyalty_id = new_loyalty_id
        self.db.add(db_customer)
        self.db.commit()

        self.db.delete(db_order)
        self.db.commit()

    def get_all_orders(self, customer_id: int) -> List[Order]:
        orders = self.db.query(Order).filter(Order.customer_id == customer_id).all()
        return orders
