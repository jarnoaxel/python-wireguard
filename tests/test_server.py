import pytest
import os

from context import python_wireguard as wg


def test_create_server():
    base64_key = "YJZ1GXi2cqGj3tMANDnk0D0k18r0x1pByzS4kP8mVEU="
    key = wg.Key(base64_key)
    server = wg.Server('wg-pytest', key, "10.0.0.1/24", 1234)
    assert isinstance(server, wg.Server)


def test_create_server_invalid_interface():
    base64_key = "YJZ1GXi2cqGj3tMANDnk0D0k18r0x1pByzS4kP8mVEU="
    key = wg.Key(base64_key)
    with pytest.raises(ValueError):
        server = wg.Server('wg pytest', key, "10.0.0.1/24", 1234)


def test_create_server_invalid_key():
    base64_key = "YJZ1GXi2cqGj3tMANDnk0D0k18r0x1pByzS4kP8mVEU="
    with pytest.raises(ValueError):
        server = wg.Server('wg-pytest', base64_key, "10.0.0.1/24", 1234)


def test_create_delete_interface(capfd):
    private, public = wg.Key.key_pair()
    server = wg.Server('wg-pytest', private, "10.0.0.1/24", 1234)

    server.create_interface()
    os.system("wg show")
    captured = capfd.readouterr()
    assert 'wg-pytest' in captured.out

    server.delete_interface()
    os.system("wg show")
    captured = capfd.readouterr()
    assert 'wg-pytest' not in captured.out


def test_add_invalid_connection():
    base64_key = "YJZ1GXi2cqGj3tMANDnk0D0k18r0x1pByzS4kP8mVEU="
    key = wg.Key(base64_key)
    server = wg.Server('wg-pytest', key, "10.0.0.1/24", 1234)
    with pytest.raises(ValueError):
        server.add_client("blah")


def test_add_valid_connection(capfd):
    private, public = wg.Key.key_pair()
    base64_key = "YJZ1GXi2cqGj3tMANDnk0D0k18r0x1pByzS4kP8mVEU="
    key = wg.Key(base64_key)
    server = wg.Server('wg-pytest', private, "10.0.0.1/24", 1234)
    server.enable()
    conn = wg.ClientConnection(key, "10.0.0.2")
    server.add_client(conn)

    os.system("wg show")
    captured = capfd.readouterr()
    text = captured.out
    assert 'wg-pytest' in text
    assert base64_key in text

    server.delete_interface()
