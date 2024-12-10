import pytest
from unittest.mock import Mock, patch, AsyncMock
from src.trading.crypto_api import CryptoAPI
import aiohttp
import json

@pytest.fixture
def mock_api_response():
    return {
        "code": 0,
        "method": "public/get-ticker",
        "result": {
            "instrument_name": "BTC_USDT",
            "bid": 50000.0,
            "ask": 50100.0,
            "last": 50050.0,
            "volume": 100.5,
            "timestamp": 1640995200000
        }
    }

@pytest.fixture
def mock_order_response():
    return {
        "code": 0,
        "method": "private/create-order",
        "result": {
            "order_id": "123456789",
            "client_oid": "my_order_123",
            "status": "ACTIVE"
        }
    }

class TestCryptoAPI:
    @pytest.mark.asyncio
    async def test_get_ticker(self, mock_api_response):
        """Test retrieving ticker data"""
        with patch('aiohttp.ClientSession.get') as mock_get:
            mock_get.return_value.__aenter__.return_value.json = AsyncMock(
                return_value=mock_api_response
            )
            
            api = CryptoAPI()
            ticker = await api.get_ticker("BTC_USDT")
            
            assert ticker["last"] == 50050.0
            assert ticker["volume"] == 100.5
            
    @pytest.mark.asyncio
    async def test_place_buy_order(self, mock_order_response):
        """Test placing a buy order"""
        with patch('aiohttp.ClientSession.post') as mock_post:
            mock_post.return_value.__aenter__.return_value.json = AsyncMock(
                return_value=mock_order_response
            )
            
            api = CryptoAPI()
            order = await api.place_order(
                symbol="BTC_USDT",
                side="BUY",
                quantity=0.1,
                price=50000.0
            )
            
            assert order["order_id"] == "123456789"
            assert order["status"] == "ACTIVE"
            
    @pytest.mark.asyncio
    async def test_place_sell_order(self, mock_order_response):
        """Test placing a sell order"""
        with patch('aiohttp.ClientSession.post') as mock_post:
            mock_post.return_value.__aenter__.return_value.json = AsyncMock(
                return_value=mock_order_response
            )
            
            api = CryptoAPI()
            order = await api.place_order(
                symbol="BTC_USDT",
                side="SELL",
                quantity=0.1,
                price=51000.0
            )
            
            assert order["order_id"] == "123456789"
            assert order["status"] == "ACTIVE"
            
    @pytest.mark.asyncio
    async def test_get_order_status(self):
        """Test retrieving order status"""
        mock_status_response = {
            "code": 0,
            "method": "private/get-order-detail",
            "result": {
                "order_id": "123456789",
                "status": "FILLED",
                "filled_quantity": 0.1,
                "filled_price": 50000.0
            }
        }
        
        with patch('aiohttp.ClientSession.get') as mock_get:
            mock_get.return_value.__aenter__.return_value.json = AsyncMock(
                return_value=mock_status_response
            )
            
            api = CryptoAPI()
            status = await api.get_order_status("123456789")
            
            assert status["status"] == "FILLED"
            assert status["filled_quantity"] == 0.1
            
    @pytest.mark.asyncio
    async def test_get_market_depth(self):
        """Test retrieving market depth"""
        mock_depth_response = {
            "code": 0,
            "method": "public/get-book",
            "result": {
                "bids": [[50000.0, 1.5], [49900.0, 2.0]],
                "asks": [[50100.0, 1.0], [50200.0, 2.5]]
            }
        }
        
        with patch('aiohttp.ClientSession.get') as mock_get:
            mock_get.return_value.__aenter__.return_value.json = AsyncMock(
                return_value=mock_depth_response
            )
            
            api = CryptoAPI()
            depth = await api.get_market_depth("BTC_USDT")
            
            assert len(depth["bids"]) == 2
            assert len(depth["asks"]) == 2
            assert depth["bids"][0][0] == 50000.0
            
    @pytest.mark.asyncio
    async def test_api_error_handling(self):
        """Test API error handling"""
        mock_error_response = {
            "code": 10004,
            "message": "API rate limit exceeded"
        }
        
        with patch('aiohttp.ClientSession.get') as mock_get:
            mock_get.return_value.__aenter__.return_value.json = AsyncMock(
                return_value=mock_error_response
            )
            
            api = CryptoAPI()
            with pytest.raises(Exception) as exc_info:
                await api.get_ticker("BTC_USDT")
            assert "API rate limit exceeded" in str(exc_info.value)
            
    @pytest.mark.asyncio
    async def test_network_error_handling(self):
        """Test network error handling"""
        with patch('aiohttp.ClientSession.get') as mock_get:
            mock_get.side_effect = aiohttp.ClientError("Network error")
            
            api = CryptoAPI()
            with pytest.raises(Exception) as exc_info:
                await api.get_ticker("BTC_USDT")
            assert "Network error" in str(exc_info.value)
