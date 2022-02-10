from context import python_wireguard as wg


def test_create_instance():
    private, public = wg.Key.key_pair()
    conn = wg.ClientConnection(public, "10.0.0.2")
    assert isinstance(conn, wg.ClientConnection)


def test_get_key():
    base64_key = "YJZ1GXi2cqGj3tMANDnk0D0k18r0x1pByzS4kP8mVEU="
    key = wg.Key(base64_key)
    conn = wg.ClientConnection(key, "10.0.0.2")
    assert str(conn.get_key()) == base64_key


def test_get_ip():
    base64_key = "YJZ1GXi2cqGj3tMANDnk0D0k18r0x1pByzS4kP8mVEU="
    key = wg.Key(base64_key)
    conn = wg.ClientConnection(key, "10.0.0.2")
    assert conn.get_ip() == "10.0.0.2"
