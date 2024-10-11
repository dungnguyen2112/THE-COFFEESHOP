from sqlalchemy.orm import Session

from models.products import Product
from schemas.products import ProductRequest, ProductUpdateRequest


class ProductService:
    def __init__(self, db: Session):
        self.db = db

    def create_product(self, product: ProductRequest):
        new_product = Product(
            name=product.name,
            description=product.description,
            price=product.price,
            stock_quantity=product.stock_quantity
        )
        self.db.add(new_product)
        self.db.commit()
        self.db.refresh(new_product)
        return new_product

    def get_product(self, product_id: int):
        product = self.db.query(Product).filter(Product.product_id == product_id).first()
        if product is None:
            raise ValueError("Product not found")
        return product

    def update_product(self, product_id: int, product_data: ProductUpdateRequest):
        product = self.db.query(Product).filter(Product.product_id == product_id).first()
        if product is None:
            raise ValueError("Product not found")

        for key, value in product_data.dict(exclude_unset=True).items():
            setattr(product, key, value)

        self.db.commit()
        self.db.refresh(product)
        return product

    def delete_product(self, product_id: int):
        product = self.db.query(Product).filter(Product.product_id == product_id).first()
        if product is None:
            raise ValueError("Product not found")

        self.db.delete(product)
        self.db.commit()

    def get_all_products(self):
        return self.db.query(Product).all()
