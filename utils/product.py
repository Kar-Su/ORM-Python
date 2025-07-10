from databases.models import Product, StatusProduct
from decimal import Decimal
from sqlalchemy.orm import Session
from .base import BaseUtils
import pandas as pd

class ProductUtils(BaseUtils):
    def __init__(self, db_session: Session):
        super().__init__(db_session, Product)

    def create(self, name: str, price: Decimal, category: str, merchant_id: int, status: StatusProduct = StatusProduct.IN_STOCK) -> Product:
        new_product = Product(Name=name, Price=price, Category=category, MerchantID=merchant_id, Status=status)
        self.db.add(new_product)
        print(f"logs: Produk '{name}' ditambahkan ke session.")
        return new_product

    def FindAs(self, **kwargs) -> pd.DataFrame:
        query_result = self.db.query(self.model).filter_by(**kwargs).all()
        if not query_result: 
            return pd.DataFrame()
        
        data = [p.__dict__ for p in query_result]
        df = pd.DataFrame(data).drop(columns=['_sa_instance_state'], errors='ignore')
        return df

    def toDataFrame(self) -> pd.DataFrame:
        all_products = self.get_all()

        if not all_products:
            print("logs: Saat ini belum ada produk yang dijual.")
            return pd.DataFrame()

        products_data = [
            {
                "ID": p.ID,
                "Nama Produk": p.Name,
                "Harga": p.Price,
                "Kategori": p.Category,
                "Status": p.Status.name if p.Status else None
            }
            for p in all_products
        ]
        
        df = pd.DataFrame(products_data).set_index("ID")
        return df
