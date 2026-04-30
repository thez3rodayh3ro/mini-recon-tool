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

# Load targets from file
def load_targets(filename):
    try:
        with open(filename, "r") as f:
            return [line.strip() for line in f if line.strip()]
    except Exception as e:
        print(f"Error loading targets: {e}")
        return []
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
     
# Get IP info using ipinfo.io API call
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
def scan_ports(target_ip, lower, upper):
    import socket
    open_ports = []
    common_ports = {21: "FTP",22: "SSH",80: "HTTP",443: "HTTPS"}
    print("\n--- OPEN PORTS ---")
    # Range of ports to scan
    for port in range(lower, upper + 1):
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
def save_results(target_ip, open_ports, response, start, target):
    try:
        with open(f"reports/scan_results_{target_ip}.txt", "w") as f:
            if len(open_ports) == 0:
                f.write("No open ports found.\n")
            else:
                f.write("\n--- Target Information ---")
                f.write(f"\nTarget: {target}")
                f.write(f"\nIP Address: {target_ip}")
                f.write(f"\nOrg: {response.get('org')}")
                f.write(f"\nLocation: {response.get('city')}, {response.get('country')}")
                f.write("\n\n--- OPEN PORTS ---\n")
                for port, service in open_ports:
                    f.write(f"{port} - {service}\n")
                # SUMMARY
                end = time.time()
                f.write("\n\n--- SUMMARY ---")
                f.write(f"\nTotal Open Ports: {len(open_ports)}")
                f.write(f"\nScan Time: {end - start:.2f} seconds")
    except Exception as e:
        print(f"Error saving results: {e}")
        return None

# MAIN FUNCTION
import time
import os
os.makedirs("reports", exist_ok=True)

# GET TARGET INPUT
targets = load_targets(input("Enter filename: "))
if not targets:
    print("No valid targets found. Exiting.")
    exit()
else:
    # GET PORT RANGE
    try:
        lower = int(input("Enter lower port range (default 20): ") or 20)
        upper = int(input("Enter upper port range (default 3306): ") or 3306)
    except ValueError as e:
        print(f"Invalid input: {e}. Using default range.")
        lower, upper = 20, 3306
    for target in targets:
        print("\n========================")
        print(f"\nProcessing target: {target}")
        target_ip = resolve_target(target)
        if not target_ip:
            print("Failed to resolve target IP.")
            continue
        # Get IP info using ipinfo.io API
        start = time.time()
        response = get_request(target_ip)
        print("\n--- TARGET INFO ---")
        print("IP:", target_ip)
        print("Org:", response.get("org"))
        print("Location:", response.get("city"), response.get("country"))

        # PORT SCANNING
        open_ports = scan_ports(target_ip, lower, upper)
        # SAVE RESULTS
        save_results(target_ip, open_ports, response, start, target)
    print("\n========================")
    print("Batch Recon Complete. Report(s) saved.") 

     


