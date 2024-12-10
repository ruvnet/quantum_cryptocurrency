from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.orm import DeclarativeBase, relationship

class Base(DeclarativeBase):
    """Base class for all mapped classes"""
    pass

class Asset(Base):
    """Model for tracking assets"""
    __tablename__ = 'assets'
    
    id = Column(Integer, primary_key=True)
    symbol = Column(String, unique=True, nullable=False)
    name = Column(String)
    current_price = Column(Float)
    last_updated = Column(DateTime)
    
    purchase_records = relationship("PurchaseRecord", back_populates="asset")

class PurchaseRecord(Base):
    """Model for tracking purchase records"""
    __tablename__ = 'purchase_records'
    
    id = Column(Integer, primary_key=True)
    asset_symbol = Column(String, ForeignKey('assets.symbol'), nullable=False)
    purchase_price = Column(Float, nullable=False)
    quantity = Column(Float, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    
    asset = relationship("Asset", back_populates="purchase_records")
