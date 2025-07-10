from databases.models import OrderProduct, Product, StatusOrder, Order
from .base import BaseUtils
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional
from decimal import Decimal

class OrderUtils(BaseUtils):
    def __init__(self, db_session: Session):
        super().__init__(db_session, Order)

    def create(self, user_id: int) -> Order:
        new_order = Order(UserID=user_id, Status=StatusOrder.WAITING_PAYMENT, CreatedAt=datetime.now())
        self.db.add(new_order)
        print(f"-> logs: Order baru untuk User ID {user_id} ditambahkan ke session.")
        return new_order

    def add(self, order_id: int, product_id: int, quantity: int) -> Optional[OrderProduct]:
        """Menambahkan produk ke dalam sebuah order."""
        product = self.db.query(Product).filter(Product.ID == product_id, Product.Status == StatusOrder.IN_STOCK).first()
        if not product:
            print(f"-> Gagal: Produk ID {product_id} tidak ada atau stok habis.")
            return None
       
        new_order_detail = OrderProduct(OrderID=order_id, ProductID=product_id, Quantity=quantity)
        self.db.add(new_order_detail)
        print(f"logs: Produk '{product.Name}' (x{quantity}) ditambahkan ke Order ID {order_id}.")
        return new_order_detail

    def getDetails(self, order_id: int) -> str:
        order = self.get_by_id(order_id)
        if not order: 
            return f"Order ID {order_id} tidak ditemukan."

        output = []
        output.append(f"\nDetail Order #{order.ID}")
        output.append(f"Pembeli : {order.user.UserName}")
        output.append(f"Status  : {order.Status.name}")
        output.append(f"Waktu   : {order.CreatedAt.strftime('%Y-%m-%d %H:%M:%S')}")
        output.append("\nDaftar Produk ")
        total = Decimal(0)
        for detail in order.product_details:
            subtotal = detail.product.Price * detail.Quantity
            total += subtotal
            output.append(f"  - {detail.product.Name} (x{detail.Quantity}) @ Rp {detail.product.Price:,.2f} = Rp {subtotal:,.2f}")
        
        if order.payment:
            output.append("\nDetail Pembayaran")
            output.append(f"Total : Rp {order.payment.Amount:,.2f}")
            output.append(f"Status : {order.payment.Status.name}")
        else:
            output.append(f"\nHARGA TOTAL : Rp {total:,.2f}")
            output.append(" Status : BELUM DIBAYAR")
        
        output.append("-" * 30)
        return "\n".join(output)
