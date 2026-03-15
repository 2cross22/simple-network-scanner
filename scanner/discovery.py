import platform
import subprocess
import socket

def is_host_up(ip: str, timeout_ms: int = 1000) -> bool:
    system = platform.system().lower()
    
    if system == "windows":
        cmd = ["ping", "-n", "1", "-w", str(timeout_ms), str(ip)]
    else:
        timeout_s = max(1, timeout_ms // 1000)
        cmd = ["ping", "-c", "1", "-W", str(timeout_s), str(ip)]
        
    try:
        result = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return result.returncode == 0
    except Exception:
        return False

def fallback_tcp_ping(ip: str, port: int = 80, timeout: float = 0.5) -> bool:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            return s.connect_ex((str(ip), port)) == 0
    except Exception:
        return False

def discover_host(ip: str) -> bool:
    if is_host_up(ip):
        return True
    
    if fallback_tcp_ping(ip, port=80) or fallback_tcp_ping(ip, port=443):
        return True
        
    return False
