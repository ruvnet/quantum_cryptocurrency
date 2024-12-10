import aiohttp
import hmac
import hashlib
import time
import os
from typing import Dict, Any
import json

class CryptoAPI:
    """Interface for Crypto.com Exchange API"""
    
    def __init__(self):
        """Initialize API client with credentials from environment"""
        self.api_key = os.getenv('CRYPTO_API_KEY')
        self.api_secret = os.getenv('CRYPTO_API_SECRET')
        self.base_url = 'https://api.crypto.com/v2'
        
    async def _request(self, method: str, endpoint: str, params: Dict = None) -> Dict:
        """Make authenticated request to API"""
        url = f"{self.base_url}/{endpoint}"
        headers = self._generate_auth_headers() if self.api_key else {}
        
        async with aiohttp.ClientSession() as session:
            try:
                if method.upper() == 'GET':
                    async with session.get(url, params=params, headers=headers) as response:
                        data = await response.json()
                else:  # POST
                    async with session.post(url, json=params, headers=headers) as response:
                        data = await response.json()
                        
                if data.get('code', 0) != 0:
                    raise Exception(f"API Error: {data.get('message', 'Unknown error')}")
                    
                return data
                
            except aiohttp.ClientError as e:
                raise Exception(f"Network error: {str(e)}")
                
    def _generate_auth_headers(self) -> Dict:
        """Generate authentication headers"""
        timestamp = int(time.time() * 1000)
        nonce = str(timestamp)
        
        if not self.api_key or not self.api_secret:
            return {}
            
        payload = f"{timestamp}{self.api_key}{nonce}"
        signature = hmac.new(
            self.api_secret.encode('utf-8'),
            payload.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        return {
            'api-key': self.api_key,
            'api-timestamp': str(timestamp),
            'api-nonce': nonce,
            'api-signature': signature
        }
        
    async def get_ticker(self, symbol: str) -> Dict:
        """Get current ticker information"""
        endpoint = 'public/get-ticker'
        params = {'instrument_name': symbol}
        response = await self._request('GET', endpoint, params)
        return response['result']
        
    async def place_order(self, symbol: str, side: str, quantity: float, price: float) -> Dict:
        """Place a new order"""
        endpoint = 'private/create-order'
        params = {
            'instrument_name': symbol,
            'side': side.upper(),
            'type': 'LIMIT',
            'quantity': quantity,
            'price': price
        }
        response = await self._request('POST', endpoint, params)
        return response['result']
        
    async def get_order_status(self, order_id: str) -> Dict:
        """Get status of an order"""
        endpoint = 'private/get-order-detail'
        params = {'order_id': order_id}
        response = await self._request('GET', endpoint, params)
        return response['result']
        
    async def get_market_depth(self, symbol: str) -> Dict:
        """Get market depth (order book)"""
        endpoint = 'public/get-book'
        params = {
            'instrument_name': symbol,
            'depth': 50  # Number of price levels
        }
        response = await self._request('GET', endpoint, params)
        return response['result']
        
    async def get_account_balance(self) -> Dict:
        """Get account balance"""
        endpoint = 'private/get-account-summary'
        response = await self._request('GET', endpoint)
        return response['result']
        
    async def cancel_order(self, order_id: str) -> Dict:
        """Cancel an existing order"""
        endpoint = 'private/cancel-order'
        params = {'order_id': order_id}
        response = await self._request('POST', endpoint, params)
        return response['result']
        
    async def get_trades(self, symbol: str) -> Dict:
        """Get recent trades"""
        endpoint = 'public/get-trades'
        params = {'instrument_name': symbol}
        response = await self._request('GET', endpoint, params)
        return response['result']
