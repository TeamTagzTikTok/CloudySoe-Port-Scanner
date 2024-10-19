import socket
import threading
import sys
import os
import time
from concurrent.futures import ThreadPoolExecutor
from colorama import init, Fore

init(autoreset=True)

def display_title():
    title = r"""
   _____ _                 _        _____
  / ____| |               | |      / ____|
 | |    | | ___  _   _  __| |_   _| (___   ___   ___
 | |    | |/ _ \| | | |/ _` | | | |\___ \ / _ \ / _ \
 | |____| | (_) | |_| | (_| | |_| |____) | (_) |  __/
  \_____|_|\___/ \__,_|\__,_|\__, |_____/ \___/ \___|
                              __/ |
  _____           _          |___/__ 
 |  __ \         | |          / ____| 
 | |__) |__  _ __| |_        | (___   ___ __ _ _ __  _ __   ___ _ __
 |  ___/ _ \| '__| __|        \___ \ / __/ _` | '_ \| '_ \ / _ \ '__|
 | |  | (_) | |  | |_         ____) | (_| (_| | | | | | | |  __/ |   
 |_|   \___/|_|   \__|       |_____/ \___\__,_|_| |_|_| |_|\___|_|   
    """
    print(Fore.CYAN + title)

def log_error(message):
    log_file_path = os.path.join(os.path.expanduser("~"), "log.txt")
    with open(log_file_path, "a") as log_file:
        log_file.write(f"{message}\n")

def ensure_log_file_exists():
    log_file_path = os.path.join(os.path.expanduser("~"), "log.txt")
    if not os.path.exists(log_file_path):
        with open(log_file_path, "w") as log_file:
            log_file.write("Log file created.\n")

def scan_port(ip, port, open_ports, closed_ports, lock, total_ports, scanned_ports):
    scanner = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    scanner.settimeout(0.5)
    try:
        result = scanner.connect_ex((ip, port))
        with lock:
            if result == 0:
                open_ports.append(port)
            else:
                closed_ports.append(port)
    except Exception as e:
        log_error(f"Error scanning {ip}:{port} - {e}")
    finally:
        scanner.close()

    with lock:
        scanned_ports[0] += 1
        progress = (scanned_ports[0] / total_ports) * 100
        sys.stdout.write(f"\rProgress: {scanned_ports[0]}/{total_ports} ports scanned ({progress:.2f}%)")
        sys.stdout.flush()

def scan_ports(ip, start_port=1, end_port=65535, max_workers=100):
    open_ports = []
    closed_ports = []
    lock = threading.Lock()
    scanned_ports = [0]
    total_ports = end_port - start_port + 1

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for port in range(start_port, end_port + 1):
            futures.append(executor.submit(scan_port, ip, port, open_ports, closed_ports, lock, total_ports, scanned_ports))

        for future in futures:
            future.result()

    return open_ports, closed_ports

if __name__ == "__main__":
    ensure_log_file_exists()
    display_title()

    time.sleep(3)

    agreement = input(Fore.WHITE + "YOU MUST HAVE PERMISSION TO DO THIS PORT SCAN, THIS IS A HACKING TECHNIQUE!\nDo You Accept? (yes/no): ").strip().lower()
    if agreement != 'yes':
        print(Fore.RED + "You must accept to proceed. Exiting...")
        sys.exit()

    try:
        threads = int(input(Fore.WHITE + "Enter the number of threads (suggested: 100): ") or 100)
    except ValueError:
        log_error("Invalid input for threads. Defaulting to 100.")
        threads = 100

    multi_machine = input(Fore.WHITE + "Do you want to scan multiple machines? (yes/no): ").lower() == 'yes'

    servers = []

    if multi_machine:
        while True:
            server = input(Fore.WHITE + "Enter server in the format 'name:ip:port' (or type 'done' to finish): ")
            if server.lower() == 'done':
                break
            try:
                name, ip, port = server.split(':')
                port = int(port)
                servers.append((name, ip, port))
            except ValueError:
                log_error("Invalid input for server. Please enter in the format 'name:ip:port'.")

    else:
        ip = input(Fore.WHITE + "Enter the server IP: ")
        port_input = input(Fore.WHITE + "Enter the port to scan (or 'all' to scan all ports): ")
        
        if port_input.lower() == 'all':
            start_port, end_port = 1, 65535
        else:
            try:
                port = int(port_input)
                start_port = end_port = port
            except ValueError:
                log_error("Invalid port number. Defaulting to scan all ports.")
                start_port, end_port = 1, 65535

        servers.append((ip, ip, start_port, end_port))

    print(Fore.GREEN + f"Threads: {threads}")
    print(Fore.GREEN + f"Multi Machine: {multi_machine}")

    all_open_ports = []

    for server in servers:
        if multi_machine:
            name, ip, port = server
            print(Fore.GREEN + f"Scanning {name}: {ip}:{port}")
            open_ports, closed_ports = scan_ports(ip, port, port, max_workers=threads)
        else:
            print(Fore.GREEN + f"Scanning {ip}:{start_port}-{end_port}")
            open_ports, closed_ports = scan_ports(ip, start_port, end_port, max_workers=threads)

        all_open_ports.extend(open_ports)

    os.system('cls' if os.name == 'nt' else 'clear')

    print(Fore.CYAN + "Scan Results:")
    if all_open_ports:
        print(Fore.GREEN + "Open Ports Found:")
        for port in all_open_ports:
            print(Fore.GREEN + f"- Port {port} is open")
    else:
        print(Fore.RED + "No open ports found.")

    input(Fore.WHITE + "Press Enter to exit...")
