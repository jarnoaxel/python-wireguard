from context import python_wireguard as wg
import pytest

def test_random():
    secret_a, public_a = wg.Key.key_pair()
    secret_b, public_b = wg.Key.key_pair()
    
    assert str(secret_a) != str(secret_b)
    assert str(public_a) != str(public_b)

def test_secret_public_different():
    secret, public = wg.Key.key_pair()
    assert str(secret) != str(public)

def test_from_base64():
    secret, public = wg.Key.key_pair()
    other_key = wg.Key(str(secret))
    assert str(secret) == str(other_key)

def test_valid_base64():
    with pytest.raises(ValueError):
        wg.Key("some random string")