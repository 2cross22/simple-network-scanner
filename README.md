# a command-line tool built to discover active devices on a local network, resolve hostnames, and scan for standard open ports.

### features

- **network detection**: automatically detects your local ip and subnet.
- **host discovery**: uses fast ping sweeps and tcp fallbacks to find devices.
- **hostname resolution**: resolves device hostnames via reverse dns.
- **port scanning**: multi-threaded scanning of common administrative ports.

### installation

```bash
pip install -r requirements.txt
```

### usage

scan your local network automatically:
```bash
python main.py --scan-local
```

scan a specific network range (cidr format):
```bash
python main.py --range 192.168.1.0/24
```

### example output

```text
detecting local network

scan results
------------
network: 10.0.0.0/24

device
ip: 10.0.0.1
hostname: router.local
ports: 80, 443

device
ip: 10.0.0.15
hostname: desktop
ports: 3389
```
