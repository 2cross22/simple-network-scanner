import socket
import concurrent.futures
from typing import List

COMMON_PORTS = [
    21, 22, 23, 25, 53, 80, 110, 135, 139, 143, 443, 445, 3389, 8080
]

def check_port(ip: str, port: int, timeout: float = 0.5) -> int | None:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            result = s.connect_ex((str(ip), port))
            if result == 0:
                return port
            return None
    except Exception:
        return None

def scan_ports(ip: str, ports: List[int] = None, timeout: float = 0.5) -> List[int]:
    if ports is None:
        ports = COMMON_PORTS
        
    open_ports = []
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(ports)) as executor:
        future_to_port = {
            executor.submit(check_port, ip, port, timeout): port 
            for port in ports
        }
        
        for future in concurrent.futures.as_completed(future_to_port):
            port = future.result()
            if port is not None:
                open_ports.append(port)
                
    return sorted(open_ports)
