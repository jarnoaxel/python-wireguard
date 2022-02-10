from context import python_wireguard as wg


def test_create_instance():
    private, public = wg.Key.key_pair()
    conn = wg.ServerConnection(public, "10.0.0.2", 1234)
    assert isinstance(conn, wg.ServerConnection)


def test_get_key():
    base64_key = "YJZ1GXi2cqGj3tMANDnk0D0k18r0x1pByzS4kP8mVEU="
    key = wg.Key(base64_key)
    conn = wg.ServerConnection(key, "10.0.0.2", 1234)
    assert str(conn.get_key()) == base64_key


def test_get_endpoint():
    base64_key = "YJZ1GXi2cqGj3tMANDnk0D0k18r0x1pByzS4kP8mVEU="
    key = wg.Key(base64_key)
    conn = wg.ServerConnection(key, "10.0.0.2", 1234)
    assert conn.get_endpoint() == "10.0.0.2"


def test_get_port():
    base64_key = "YJZ1GXi2cqGj3tMANDnk0D0k18r0x1pByzS4kP8mVEU="
    key = wg.Key(base64_key)
    conn = wg.ServerConnection(key, "10.0.0.2", 1234)
    assert conn.get_port() == 1234
