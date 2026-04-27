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

# INPUT TARGET
import socket
import time

open_ports = []
target = input("Enter target:")

try:
    target_ip = socket.gethostbyname(target)
    #print(target_ip)
except:
    print("Invalid target")
    exit()
start = time.time()

# PORT SCANNING
common_ports = {21: "FTP",22: "SSH",80: "HTTP",443: "HTTPS"}

for port in range(20,444):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.5)
    try:
        result = sock.connect_ex((target_ip, port))

        if result == 0:
            print(f"PORT {port} {common_ports[port]} is OPEN")
            service = common_ports[port]
            open_ports.append((port,service))
    except Exception as e:
            print(f"Error on port {port}: {e}")
    finally:
            sock.close() 

# SAVE RESULTS

with open(f"scan_results_{target_ip}.txt", "w") as f:
    for port, service in open_ports:
        f.write(f"{port} - {service}\n")
    # SUMMARY
    end = time.time()
    f.write("\n--- SUMMARY ---")
    f.write(f"\nTotal Open Ports: {len(open_ports)}")
    f.write(f"\nScan Time: {end - start:.2f} seconds")
