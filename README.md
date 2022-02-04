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
from python_wireguard import Key
private, public = Key.key_pair()
public
# <python_wireguard.Key object: 5TxYUa403l9A9yEVMyIsSZwae4C7497IT8uaMYEdLHQ=>
print(public)
# 5TxYUa403l9A9yEVMyIsSZwae4C7497IT8uaMYEdLHQ=
```

Creating a key from a base64 string is also possible, which is useful for creating one for the other device's public key:
```python
from python_wireguard import Key
srv_public = Key("some string containing a base64 key")
```

### Server
```python
from python_wireguard import Server, ClientConnection
server = Server("wg-srv", private, 12345, "10.0.0.1/24")
server.enable()
```
You should now be able to see connection on your machine using the 'normal' wireguard cli:
```shell
sudo wg
```
Example output:
```
interface: wg-srv
  public key: Z9mHJ0apfgTvULpV3t9jpzyjmABSts1weE2jPiee8w8=
  private key: (hidden)
  listening port: 12345
```
#### Add a client

### Client
```python
wg.setup_client_connection("wg-client", private, "10.0.0.2/24", srv_public, "public ip of VPN server", 12345)
wg.enable_device("wg-client")
```