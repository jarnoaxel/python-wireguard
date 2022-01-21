# Python Wireguard interface
Library for controlling Wireguard using python.

## Installation
In order to use this package, you need to build it.
```bash
cd c
make
cd ..
```
For the python part, there are some dependencies:
```bash
cd py
pip install -r requirements.txt
```

## Security remark
Changing network interface settings, and interacting with Wireguard, is only possible as the root user by default. Of course, this is not secure to run like this in a production environment (the demo server is not secured in any way either). You should make sure that you secure your server appropriately (keeping the parts of your application that need to interact with Wireguard in a container that is used for nothing else, for instance). For demo purposes, you can run the scripts using `sudo` or as the root user.

## Usage
For demo usage, you need two machines.

### Server
One of the machines (the server) should be publicly accessible over the internet. On this machine, copy `.env.example` to `.env` and set the following values:

```
SERVER_IP= # Here you need to enter the public ip of the server
WG_PORT= # Here you need to choose a port on which Wireguard will listen. Make sure that it is open! (Wireguard uses udp so you only have to open it for udp traffic)
HTTP_PORT= # Here you need to specify a port for the http server. For instance, 8888
INTERNET_INTERFACE= # This is the default network interface of the server. Usually eth0, but it could be something different (check with `ip a` or `ifconfig` depending on your distro)
WG_INTERFACE= # Choose a name for the Wireguard network interface name. Like `wg0`, or `wg-srv`
```

You can now start the server:
```bash
sudo ./test_srv.py
```

### Client
On the client machine, run the following command to connect:
```bash
sudo ./test_client.py connect http://{server_ip_address}:{server_port}
```

To disconnect, run the following command:
```bash
sudo ./test_client.py disconnect
```
