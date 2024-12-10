import pytest
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from src.trading.models import Base, PurchaseRecord, Asset
from datetime import datetime

@pytest.fixture
def test_db():
    """Create a test database"""
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()

class TestDatabaseOperations:
    def test_create_purchase_record(self, test_db):
        """Test creating a purchase record"""
        record = PurchaseRecord(
            asset_symbol='BTC',
            purchase_price=50000.0,
            quantity=0.1,
            timestamp=datetime(2024, 1, 1)
        )
        test_db.add(record)
        test_db.commit()
        
        saved_record = test_db.query(PurchaseRecord).first()
        assert saved_record.asset_symbol == 'BTC'
        assert saved_record.purchase_price == 50000.0
        
    def test_update_purchase_record(self, test_db):
        """Test updating a purchase record"""
        record = PurchaseRecord(
            asset_symbol='ETH',
            purchase_price=2000.0,
            quantity=1.0,
            timestamp=datetime(2024, 1, 1)
        )
        test_db.add(record)
        test_db.commit()
        
        record.purchase_price = 2100.0
        test_db.commit()
        
        updated_record = test_db.query(PurchaseRecord).first()
        assert updated_record.purchase_price == 2100.0
        
    def test_retrieve_purchase_history(self, test_db):
        """Test retrieving purchase history for an asset"""
        records = [
            PurchaseRecord(
                asset_symbol='BTC',
                purchase_price=price,
                quantity=0.1,
                timestamp=datetime(2024, 1, i)
            )
            for i, price in enumerate([50000.0, 51000.0, 52000.0], 1)
        ]
        test_db.add_all(records)
        test_db.commit()
        
        btc_records = test_db.query(PurchaseRecord).filter_by(asset_symbol='BTC').all()
        assert len(btc_records) == 3
        assert all(record.asset_symbol == 'BTC' for record in btc_records)
        
    def test_average_purchase_price(self, test_db):
        """Test calculating average purchase price"""
        records = [
            PurchaseRecord(
                asset_symbol='BTC',
                purchase_price=price,
                quantity=0.1,
                timestamp=datetime(2024, 1, i)
            )
            for i, price in enumerate([50000.0, 51000.0, 52000.0], 1)
        ]
        test_db.add_all(records)
        test_db.commit()
        
        avg_price = (
            test_db.query(func.avg(PurchaseRecord.purchase_price))
            .filter_by(asset_symbol='BTC')
            .scalar()
        )
        assert avg_price == 51000.0  # (50000 + 51000 + 52000) / 3
