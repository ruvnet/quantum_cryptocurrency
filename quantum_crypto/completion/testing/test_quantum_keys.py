import pytest
from quantum_crypto.quantum_currency.quantum_keygen import (
    generate_quantum_keypair,
    sign_message,
    verify_signature
)
import numpy as np

def test_keypair_generation():
    """Test quantum keypair generation"""
    public_key, private_key = generate_quantum_keypair()
    
    assert isinstance(public_key, bytes)
    assert isinstance(private_key, bytes)
    assert len(public_key) > 0
    assert len(private_key) > 0
    assert public_key != private_key

def test_signature_verification():
    """Test message signing and verification"""
    public_key, private_key = generate_quantum_keypair()
    message = b"test message"
    
    # Sign message
    signature = sign_message(message, private_key)
    assert isinstance(signature, bytes)
    
    # Verify signature
    is_valid = verify_signature(message, signature, public_key)
    assert is_valid

def test_invalid_signature():
    """Test detection of invalid signatures"""
    public_key, private_key = generate_quantum_keypair()
    message = b"test message"
    wrong_message = b"wrong message"
    
    # Sign original message
    signature = sign_message(message, private_key)
    
    # Verify with wrong message
    is_valid = verify_signature(wrong_message, signature, public_key)
    assert not is_valid

def test_tampered_signature():
    """Test detection of tampered signatures"""
    public_key, private_key = generate_quantum_keypair()
    message = b"test message"
    
    # Sign message
    signature = sign_message(message, private_key)
    
    # Tamper with signature
    tampered_signature = bytearray(signature)
    tampered_signature[0] ^= 0xFF  # Flip bits in first byte
    
    # Verify tampered signature
    is_valid = verify_signature(message, bytes(tampered_signature), public_key)
    assert not is_valid

def test_wrong_key():
    """Test verification with wrong public key"""
    public_key1, private_key1 = generate_quantum_keypair()
    public_key2, _ = generate_quantum_keypair()
    message = b"test message"
    
    # Sign with key1
    signature = sign_message(message, private_key1)
    
    # Verify with key2
    is_valid = verify_signature(message, signature, public_key2)
    assert not is_valid

def test_large_message():
    """Test signing and verification of large messages"""
    public_key, private_key = generate_quantum_keypair()
    large_message = b"x" * 1000000  # 1MB message
    
    # Sign and verify large message
    signature = sign_message(large_message, private_key)
    is_valid = verify_signature(large_message, signature, public_key)
    assert is_valid
