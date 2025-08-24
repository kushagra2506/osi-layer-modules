#!/usr/bin/env python3
import subprocess
from scapy.all import get_if_list, get_if_hwaddr

def get_interface():
    """List available interfaces and let user choose one"""
    ifaces = get_if_list()
    print("Available interfaces:")
    for i, iface in enumerate(ifaces):
        print(f"{i+1}. {iface}")
    selection = int(input("Select interface number: ")) - 1
    return ifaces[selection]

def spoof_mac(interface, new_mac):
    """Change the MAC address of the interface"""
    old_mac = get_if_hwaddr(interface)
    print(f"[*] Current MAC for {interface}: {old_mac}")

    try:
        # Bring interface down
        subprocess.run(["sudo", "ip", "link", "set", "dev", interface, "down"], check=True)
        # Change MAC
        subprocess.run(["sudo", "ip", "link", "set", "dev", interface, "address", new_mac], check=True)
        # Bring interface up
        subprocess.run(["sudo", "ip", "link", "set", "dev", interface, "up"], check=True)

        updated_mac = get_if_hwaddr(interface)
        if updated_mac.lower() == new_mac.lower():
            print(f"[+] MAC successfully changed to {new_mac}")
        else:
            print(f"[-] Failed to change MAC. Still {updated_mac}")

    except Exception as e:
        print(f"[!] Error: {e}")

if __name__ == "__main__":
    iface = get_interface()
    new_mac = input("Enter new MAC address (format: XX:XX:XX:XX:XX:XX): ")
    spoof_mac(iface, new_mac)
