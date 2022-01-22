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
To do

### Generate key pair
```python
import python_wireguard as wg
private, public = wg.key_pair()

print(wg.key_to_base64(public))
```

### Server
To do.

### Client
To do.