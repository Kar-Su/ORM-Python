from __future__ import annotations
from typing import List, Optional, Dict, Any
from datetime import datetime
from decimal import Decimal
import enum
from sqlalchemy import (Integer, String, Enum as SAenum, TIMESTAMP, ForeignKey, text, DECIMAL, Table, Column)
from sqlalchemy.orm import (relationship, Mapped, mapped_column)
from .basemodel import base


class StatusProduct(enum.Enum):
    IN_STOCK = 'IN_STOCK'
    OUT_STOCK = 'OUT_STOCK'


class StatusOrder(enum.Enum):
    WAITING_PAYMENT = 'WAITING_PAYMENT'
    PROCESSING = 'PROCESSING'
    SHIPPED = 'SHIPPED'


class StatusPayment(enum.Enum):
    PENDING = 'PENDING'
    PAID = 'PAID'
    EXPIRED = 'EXPIRED'
    REFUNDED = 'REFUNDED'


_UserLocation = Table('users_locations', base.metadata,
                      Column('UsersID', Integer, ForeignKey('users.ID'), primary_key=True), 
                      Column('LocationsID', Integer, ForeignKey('locations.ID'), primary_key=True))

class User(base):
    __tablename__ = "users"

    ID: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    UserName: Mapped[Optional[str]] = mapped_column(String(25))
    Email: Mapped[str] = mapped_column(String(25), unique=True, index=True)
    CreatedAt: Mapped[datetime] = mapped_column(TIMESTAMP)

    # Relasi location
    locations: Mapped[List["Location"]] = relationship(secondary=_UserLocation, back_populates='users')

    # Relasi merchant
    merchant: Mapped["Merchant"] = relationship(back_populates='admin')

    # Relasi order
    orders: Mapped[List["Order"]] = relationship(back_populates='user')

    def __repr__(self) -> Dict[str, Any]:
        return {'ID': self.ID, 'UserName': self.UserName, 'Email': self.Email, 'CreatedAt': self.CreatedAt}




class Location(base):
    __tablename__ = "locations"

    ID: Mapped[int] = mapped_column(Integer, primary_key=True)
    Province: Mapped[Optional[str]] = mapped_column(String(25))
    City: Mapped[Optional[str]] = mapped_column(String(25))
    ZipCode: Mapped[Optional[str]] = mapped_column(String(5))
    
    # Relasi user
    users: Mapped[List["User"]] = relationship(secondary=_UserLocation, back_populates='locations')

    #Relasi merchant
    merchant: Mapped["Merchant"] = relationship(back_populates='location')

    def __repr__(self) -> Dict[str, Any]:
        return {'ID': self.ID, 'Province': self.Province, 'City': self.City, 'ZipCode': self.ZipCode}
    

class Merchant(base):
    __tablename__ = "merchants"

    ID: Mapped[int] = mapped_column(primary_key=True)

    #Relasi user
    AdminID: Mapped[Optional[int]] = mapped_column(ForeignKey('users.ID'), unique=True)
    admin: Mapped[Optional["User"]] = relationship(back_populates='merchant')

    #Relasi location
    LocationID: Mapped[int] = mapped_column(ForeignKey('locations.ID'))
    location: Mapped["Location"] = relationship(back_populates='merchant')

    # Relasi product
    products: Mapped[List["Product"]] = relationship(back_populates='merchant')

    def __repr__(self) -> Dict[str, Any]:
        return {'ID': self.ID, 'AdminID': self.AdminID, 'LocationID': self.LocationID}



class Product(base):
    __tablename__ = "products"

    ID: Mapped[int] = mapped_column(primary_key=True)
    Name: Mapped[Optional[str]] = mapped_column(String(25))
    Price: Mapped[Optional[Decimal]] = mapped_column(DECIMAL(12, 2))
    Status: Mapped[Optional[str]] = mapped_column(SAenum(StatusProduct, name= 'status_product'), index=True)
    Category: Mapped[Optional[str]] = mapped_column(String(25), index=True)

    # Relasi merchant
    MerchantID: Mapped[int] = mapped_column(ForeignKey('merchants.ID'), index=True)
    merchant: Mapped["Merchant"] = relationship(back_populates='products')

    #Relasi order detail
    order_details: Mapped[List["OrderProduct"]] = relationship(back_populates='product')

    def __repr__(self) -> Dict[str, Any]:
        return {'ID': self.ID, 'Name': self.Name, 'Price': self.Price, 'Status': self.Status, 'Category': self.Category, 'MerchantID': self.MerchantID}


class OrderProduct(base):
    __tablename__ = "order_products"
    
    Quantity: Mapped[Optional[int]]

    # Relasi product
    ProductID: Mapped[int] = mapped_column(ForeignKey('products.ID'), primary_key=True)
    product: Mapped["Product"] = relationship(back_populates='order_details')

    # Relasi order
    OrderID: Mapped[int] = mapped_column(ForeignKey('orders.ID'), primary_key=True)
    order: Mapped["Order"] = relationship(back_populates='product_details')


class Order(base):
    __tablename__ = "orders"

    ID: Mapped[int] = mapped_column(primary_key=True)
    Status: Mapped[Optional[str]] = mapped_column(SAenum(StatusOrder, name= 'status_order'))
    CreatedAt: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))

    # Relasi user
    UserID: Mapped[int] = mapped_column(ForeignKey('users.ID'))
    user: Mapped["User"] = relationship(back_populates='orders')

    # Relasi product detail
    product_details: Mapped[List["OrderProduct"]] = relationship(back_populates='order')

    # Relasi payment
    payment: Mapped["Payment"] = relationship(back_populates='order')

    def __repr__(self) -> Dict[str, Any]:
        return {'ID': self.ID, 'Status': self.Status, 'CreatedAt': self.CreatedAt, 'UserID': self.UserID}


class Payment(base):
    __tablename__ = "payments"

    ID: Mapped[int] = mapped_column(primary_key=True)
    GatewayToken: Mapped[str] = mapped_column(String(100), unique=True)
    Amount: Mapped[Optional[Decimal]] = mapped_column(DECIMAL(12, 2))
    Status: Mapped[Optional[str]] = mapped_column(SAenum(StatusPayment, name= 'status_product'))
    PaidAt: Mapped[datetime] = mapped_column(TIMESTAMP)

    # Relasi order
    OrderID: Mapped[int] = mapped_column(ForeignKey('orders.ID'), unique=True)
    order: Mapped["Order"] = relationship(back_populates='payment')

    def __repr__(self) -> Dict[str, Any]:
        return{'ID': self.ID, 'GatewayToken': self.GatewayToken, 'Amount': self.Amount, 'Status': self.Status, 'PaidAt': self.PaidAt, 'OrderID': self.OrderID}
