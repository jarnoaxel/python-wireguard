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
This section explains setting up the connection on the server machine.

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
For adding a client connection, you first need to create a `ClientConnection` object:
```python
from python_wireguard import ClientConnection, Key

client_key = Key("base64 string received from client (public key)")
client_ip = "10.0.0.2" # The 'local' ip address that the client will be assigned.
conn = ClientConnection(client_key, client_ip)
```

You can now add this client to the server:
```python
server.add_client(conn)
```

### Client
This section explains setting up the connection on a client machine. This needs to be a different machine than the server machine.
```python
from python_wireguard import Client, ServerConnection, Key

local_ip = "10.0.0.2/24" # CIDR block received from server.

client = Client('wg-client', private, local_ip)

srv_key = Key("base64 string received from the server (public key)")
endpoint = "public ip address of the server"
port = 12345 # The port on which the server has been set up to listen

server_conn = ServerConnection(srv_key, endpoint, port)

client.set_server(server_conn)
client.connect()
```