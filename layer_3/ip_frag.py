from scapy.all import *

target_ip = "Enter Target: "  # Change to your target in LAN

# Create a large payload so it will be split into fragments
payload = b"A" * 2000  # 2000 bytes > MTU

# Build the packet
packet = IP(dst=target_ip) / ICMP() / payload

# Send fragmented packets
frags = fragment(packet, fragsize=500)  # Each fragment = 500 bytes
for i, frag in enumerate(frags):
    send(frag, verbose=False)
    print(f"Sent fragment {i+1}/{len(frags)}")
