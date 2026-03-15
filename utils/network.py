import socket
import ipaddress

def get_local_ip() -> str:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
        return ip
    except Exception:
        return "127.0.0.1"

def get_local_subnet() -> str:
    ip = get_local_ip()
    if ip == "127.0.0.1":
        return "127.0.0.0/8"
    
    network = ipaddress.IPv4Network(f"{ip}/24", strict=False)
    return str(network)
