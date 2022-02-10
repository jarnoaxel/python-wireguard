from context import wireguard
import os
import io
from wurlitzer import pipes


def test_valid_interface():
    assert wireguard.valid_interface('wg0') is True
    assert wireguard.valid_interface('contains space') is False


def test_empty_key():
    key = wireguard.empty_key()
    assert len(key) == 33


def test_key_pair():
    private, public = wireguard.key_pair()
    assert len(private) == len(public)


def test_create_server_delete(capfd):
    wireguard.delete_device('wg-pytest')
    private, public = wireguard.key_pair()
    wireguard.create_server('wg-pytest', 4242, private, "10.42.42.1/24")
    wireguard.enable_device('wg-pytest')
    os.system("wg show")
    captured = capfd.readouterr()
    assert 'wg-pytest' in captured.out
    base64_key = "YJZ1GXi2cqGj3tMANDnk0D0k18r0x1pByzS4kP8mVEU="
    other_public = wireguard.key_from_base64(base64_key)
    wireguard.server_add_peer('wg-pytest', other_public, "10.0.0.2")
    os.system("wg show")
    captured = capfd.readouterr()
    assert base64_key in captured.out
    wireguard.delete_device('wg-pytest')
    os.system("wg show")
    captured = capfd.readouterr()
    assert 'wg-pytest' not in captured.out


def test_create_server_invalid_name(capfd):
    private, public = wireguard.key_pair()
    wireguard.create_server('invalid name', 4242, private, "10.42.42.1/24")
    captured = capfd.readouterr()
    text = captured.out
    assert 'invalid device name' in text


def test_create_client_delete(capfd):
    wireguard.delete_device('wg-pytest')
    private, public = wireguard.key_pair()
    base64_key = "YJZ1GXi2cqGj3tMANDnk0D0k18r0x1pByzS4kP8mVEU="
    other_public = wireguard.key_from_base64(base64_key)
    wireguard.create_client('wg-pytest', private, "10.42.42.1/24")
    os.system("wg show")
    captured = capfd.readouterr()
    assert 'wg-pytest' in captured.out
    with pipes() as (out, err):
        wireguard.list_devices()
    assert 'wg-pytest' in out.read()
    wireguard.client_add_peer('wg-pytest', other_public, "10.1.2.7", 12345)
    os.system("wg show")
    captured = capfd.readouterr()
    assert base64_key in captured.out
    wireguard.delete_device('wg-pytest')
    os.system("wg show")
    captured = capfd.readouterr()
    assert 'wg-pytest' not in captured.out


def test_create_client_invalid_name(capfd):
    private, public = wireguard.key_pair()
    wireguard.create_client('invalid name', private, "10.42.42.1/24")
    captured = capfd.readouterr()
    text = captured.out
    assert 'invalid device name' in text


def test_enable_device_invalid(capfd):
    wireguard.enable_device("invalid name")
    captured = capfd.readouterr()
    text = captured.out
    assert 'invalid device' in text
