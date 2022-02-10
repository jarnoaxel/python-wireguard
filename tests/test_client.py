import pytest
import os

from context import python_wireguard as wg


def test_create_client():
    base64_key = "YJZ1GXi2cqGj3tMANDnk0D0k18r0x1pByzS4kP8mVEU="
    key = wg.Key(base64_key)
    client = wg.Client('wg-pytest', key, "10.0.0.1/24")
    assert isinstance(client, wg.Client)


def test_create_client_invalid_interface():
    base64_key = "YJZ1GXi2cqGj3tMANDnk0D0k18r0x1pByzS4kP8mVEU="
    key = wg.Key(base64_key)
    with pytest.raises(ValueError):
        client = wg.Client('wg pytest', key, "10.0.0.1/24")


def test_create_client_invalid_key():
    base64_key = "YJZ1GXi2cqGj3tMANDnk0D0k18r0x1pByzS4kP8mVEU="
    with pytest.raises(ValueError):
        client = wg.Client('wg-pytest', base64_key, "10.0.0.1/24")


def test_create_delete_interface(capfd):
    private, public = wg.Key.key_pair()
    client = wg.Client('wg-pytest', private, "10.0.0.1/24")

    client.create_interface()
    os.system("wg show")
    captured = capfd.readouterr()
    assert 'wg-pytest' in captured.out

    client.delete_interface()
    os.system("wg show")
    captured = capfd.readouterr()
    assert 'wg-pytest' not in captured.out


def test_connect_no_connection():
    base64_key = "YJZ1GXi2cqGj3tMANDnk0D0k18r0x1pByzS4kP8mVEU="
    key = wg.Key(base64_key)
    client = wg.Client('wg-pytest', key, "10.0.0.1/24")
    with pytest.raises(ValueError):
        client.connect()


def test_set_invalid_connection():
    base64_key = "YJZ1GXi2cqGj3tMANDnk0D0k18r0x1pByzS4kP8mVEU="
    key = wg.Key(base64_key)
    client = wg.Client('wg-pytest', key, "10.0.0.1/24")
    with pytest.raises(ValueError):
        client.set_server("blah")


def test_set_connection_connect(capfd):
    wg.delete_device('wg-pytest')
    private, public = wg.Key.key_pair()
    base64_key = "YJZ1GXi2cqGj3tMANDnk0D0k18r0x1pByzS4kP8mVEU="
    srv_public = wg.Key(base64_key)
    client = wg.Client('wg-pytest', private, "10.0.0.2/24")
    conn = wg.ServerConnection(srv_public, "127.0.0.1", 12345)
    client.set_server(conn)
    client.connect()

    os.system("wg show")
    captured = capfd.readouterr()
    text = captured.out
    assert 'wg-pytest' in text
    assert base64_key in text

    client.delete_interface()
