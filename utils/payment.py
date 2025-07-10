from databases.models import Payment, StatusPayment, StatusOrder, Order
from .base import BaseUtils
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime
import secrets


class PaymentUtils(BaseUtils):
    def __init__(self, db_session: Session):
        super().__init__(db_session, Payment)

    def create(self, order_id: int) -> Optional[Payment]:
        order = self.db.query(Order).filter(Order.ID == order_id).first()
        if not order:
            print(f"->Gagal Bayar: Order ID {order_id} tidak ditemukan.")
            return None

        total_amount = sum(detail.product.Price * detail.Quantity for detail in order.product_details)
        
        new_payment = Payment(
            OrderID=order_id,
            Amount=total_amount,
            GatewayToken=''.join(secrets.token_hex(16)),
            Status=StatusPayment.PAID,
            PaidAt=datetime.now()
        )
        order.Status = StatusOrder.PROCESSING # Update status order
        self.db.add(new_payment)
        print(f"logs: Pembayaran untuk Order ID {order_id} sebesar Rp {total_amount:,.2f} ditambahkan ke session.")
        return new_payment

