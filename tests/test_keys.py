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


def test_invalid_base64():
    with pytest.raises(ValueError):
        wg.Key("some random string")


def test_valid_base64():
    base64_key = "YJZ1GXi2cqGj3tMANDnk0D0k18r0x1pByzS4kP8mVEU="
    key = wg.Key(base64_key)
    assert str(key) == base64_key


def test_empty_key():
    empty_base64 = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA="
    empty_key = wg.Key()
    assert str(empty_key) == empty_base64


def test_repr():
    base64_key = "YJZ1GXi2cqGj3tMANDnk0D0k18r0x1pByzS4kP8mVEU="
    key = wg.Key(base64_key)
    assert base64_key in key.__repr__()


def test_byte_count():
    private, public = wg.Key.key_pair()
    assert len(private.as_bytes()) == 33
