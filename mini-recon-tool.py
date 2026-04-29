# ============================================
# Licensed under the MIT License.
# See LICENSE file in the project root for full license information.

# Mini Recon Tool (Python)
# Author: Rahul DasGupta
# Copyright (c) 2026 Rahul DasGupta
#
# This project is created for educational and
# ethical cybersecurity learning purposes only.
#
# Permission is granted to use, copy, and modify
# this code for personal and educational use.
#
# Unauthorized use of this tool against systems
# without explicit permission is illegal.
#
# The author is not responsible for any misuse
# or damage caused by this software.
# ============================================

# Resolve target to IP address
def resolve_target(target):
     import socket
     try:
          # RESOLVE TARGET TO IP ADDRESS
          sock = socket.gethostbyname(target)
          return sock
     except Exception as e:
          print(f"Error resolving target: {e}")
          return None
     
# Get IP info using ipinfo.io API
def get_request(target_ip):
    import requests
    try:
        # MAKE API CALL
        response = requests.get(f"https://ipinfo.io/{target_ip}/json").json()
    except Exception as e:
        print(f"Error fetching IP info: {e}")
        response = {}
    return response

# PORT SCANNING
def scan_ports(target_ip):
    import socket
    open_ports = []
    common_ports = {21: "FTP",22: "SSH",80: "HTTP",443: "HTTPS"}
    print("\n--- OPEN PORTS ---")
    
    for port in range(20,444):
        # CREATE SOCKET
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        try:
            # CONNECT TO PORT
            result = sock.connect_ex((target_ip, port))
            if result == 0:
                print(f"PORT {port} {common_ports[port]} is OPEN")
                
                # GET SERVICE NAME
                service = common_ports[port]

                # APPEND OPEN PORTS
                open_ports.append((port,service))
        except Exception as e:
                print(f"Error on port: {e}")
        finally:
                sock.close()
    return open_ports

# SAVE RESULTS
def save_results(target_ip, open_ports, response, start):
    try:
        with open(f"scan_results_{target_ip}.txt", "w") as f:
            if len(open_ports) == 0:
                f.write("No open ports found.\n")
            else:
                f.write("--- OPEN PORTS ---\n")
                for port, service in open_ports:
                    f.write(f"{port} - {service}\n")
                # SUMMARY
                end = time.time()
                f.write("\n--- Target Information ---")
                f.write(f"\nIP Address: {target_ip}")
                f.write(f"\nOrg: {response.get('org')}")
                f.write(f"\nLocation: {response.get('city')}, {response.get('country')}")
                f.write("\n\n--- SUMMARY ---")
                f.write(f"\nTotal Open Ports: {len(open_ports)}")
                f.write(f"\nScan Time: {end - start:.2f} seconds")
    except Exception as e:
        print(f"Error saving results: {e}")
        return None

# MAIN FUNCTION
import time
start = time.time()
target = input("Enter target:")
# Resolve target to IP address
target_ip = resolve_target(target)
if not target_ip:
    exit()
# Get IP info using ipinfo.io API
response = get_request(target_ip)
print("\n--- TARGET INFO ---")
print("IP:", target_ip)
print("Org:", response.get("org"))
print("Location:", response.get("city"), response.get("country"))

# PORT SCANNING
open_ports = scan_ports(target_ip) 
# SAVE RESULTS
save_results(target_ip, open_ports, response, start) 

print("Recon Complete. Report saved.") 



