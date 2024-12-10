import pytest
from src.quantum_currency.quantum_keygen import generate_quantum_keys, verify_signature

def test_key_generation():
    """Test quantum-resistant key pair generation"""
    private_key, public_key = generate_quantum_keys()
    assert private_key is not None, "Private key should be generated"
    assert public_key is not None, "Public key should be generated"
    assert len(private_key) >= 256, "Private key should be sufficiently long"

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
