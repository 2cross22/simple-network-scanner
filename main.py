import argparse
import ipaddress
import concurrent.futures
from rich.console import Console

from utils import network
from scanner import discovery, hostname, portscan

console = Console()

def scan_network(network_cidr: str, max_workers: int = 50):
    try:
        net = ipaddress.IPv4Network(network_cidr, strict=False)
        hosts = [str(ip) for ip in net.hosts()]
    except ValueError as e:
        console.print(f"[bold red]invalid network range: {e}[/bold red]")
        return
        
    console.print(f"\n[bold blue]scan results[/bold blue]")
    console.print(f"[bold blue]{'-'*12}[/bold blue]")
    console.print(f"network: [bold white]{network_cidr}[/bold white]\n")
    
    active_hosts = []
    
    with console.status(f"[cyan]discovering hosts in {network_cidr}[/cyan]"):
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_ip = {
                executor.submit(discovery.discover_host, ip): ip 
                for ip in hosts
            }
            
            for future in concurrent.futures.as_completed(future_to_ip):
                ip = future_to_ip[future]
                try:
                    if future.result():
                        active_hosts.append(ip)
                except Exception:
                    pass
                    
    active_hosts.sort(key=lambda ip: ipaddress.IPv4Address(ip))
    
    if not active_hosts:
        console.print("[bold yellow]no devices found on the network.[/bold yellow]")
        return
        
    with console.status(f"[cyan]scanning {len(active_hosts)} devices[/cyan]"):
        for ip in active_hosts:
            host_name = hostname.resolve_hostname(ip)
            open_ports = portscan.scan_ports(ip)
            
            if open_ports:
                ports_str = ", ".join(map(str, open_ports))
            else:
                ports_str = "none"
            
            console.print("[bold green]device[/bold green]")
            console.print(f"ip: {ip}")
            console.print(f"hostname: {host_name}")
            console.print(f"ports: {ports_str}")
            console.print()

def main():
    parser = argparse.ArgumentParser(
        description="network discovery tool."
    )
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--scan-local", 
        action="store_true", 
        help="scan the local network."
    )
    group.add_argument(
        "--range", 
        type=str, 
        metavar="CIDR",
        help="network range to scan."
    )
    
    args = parser.parse_args()
    
    if args.scan_local:
        console.print("[cyan]detecting local network[/cyan]")
        local_subnet = network.get_local_subnet()
        scan_network(local_subnet)
    elif args.range:
        scan_network(args.range)

if __name__ == "__main__":
    main()
