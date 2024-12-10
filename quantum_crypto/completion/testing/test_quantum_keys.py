import pytest
from src.quantum_currency.quantum_keygen import (
    generate_quantum_keys,
    sign_message,
    verify_signature
)

def test_key_generation():
    """Test quantum-resistant key pair generation"""
    private_key, public_key = generate_quantum_keys()
    assert private_key is not None, "Private key should be generated"
    assert public_key is not None, "Public key should be generated"
    assert hasattr(private_key, "sign"), "Private key should have sign method"
    assert hasattr(public_key, "verify"), "Public key should have verify method"

def test_signature_verification():
    """Test signature creation and verification"""
    private_key, public_key = generate_quantum_keys()
    message = "test_transaction"
    signature = sign_message(message, private_key)
    assert verify_signature(message, signature, public_key), "Valid signature should verify"

def test_invalid_signature():
    """Test that invalid signatures are rejected"""
    private_key, public_key = generate_quantum_keys()
    message = "test_transaction"
    wrong_message = "wrong_transaction"
    signature = sign_message(message, private_key)
    assert not verify_signature(wrong_message, signature, public_key), "Invalid signature should not verify"

def test_different_keys_rejection():
    """Test that signatures don't verify with different keys"""
    private_key1, _ = generate_quantum_keys()
    _, public_key2 = generate_quantum_keys()
    
    message = "test_transaction"
    signature = sign_message(message, private_key1)
    assert not verify_signature(message, signature, public_key2), "Signature should not verify with different key pair"
