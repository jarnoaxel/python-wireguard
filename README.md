# Python Wireguard interface
Library for controlling Wireguard using python.

## Installation
To install this package, use pip:

```bash
pip install python_wireguard
```

## Security remark
Changing network interface settings, and interacting with Wireguard, is only possible as the root user by default.

## Usage
This package was designed with a client/server infrastructure in mind. This differs from the 'default' usage of Wireguard, which is peer to peer. Because of this, there is a different set of functions required depending on whether you are writing client-side code or server-side code. We will now discuss an example workflow for setting up a client-server connection to Wireguard.

### Generate key pair
Both the client and the server need a key pair.

```python
import python_wireguard as wg
private, public = wg.key_pair()
```

By default the key is an array of bytes. In order to make it more usable, you can convert it to a base64 string:

```python
string = wg.key_to_base64(public)
print(string)
```

Creating a key from a base64 string is also possible, which is useful for creating one for the other device's public key:
```python
srv_public = wg.key_from_base64("some string containing a base64 key")
```

### Server
```python
wg.create_server("wg-srv", 12345, private, "10.0.0.1/24")
wg.enable_device("wg-srv")
wg.server_add_peer("wg-srv", client_public, "10.0.0.2")

```

### Client
```python
wg.setup_client_connection("wg-client", private, "10.0.0.2/24", srv_public, "public ip of VPN server", 12345)
wg.enable_device("wg-client")
```