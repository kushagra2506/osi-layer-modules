from scapy.all import IP, ICMP, send
import time

target_ip = input("Enter the ip: ")  # Change to your target in same network

for i in range(10):  # Send 10 pings
    packet = IP(dst=target_ip, ttl=64) / ICMP(id=0x1234, seq=i) / b"HELLOTEST"
    send(packet, verbose=False)
    print(f"Sent packet {i+1}")
    time.sleep(0.2)  # Small delay so Wireshark can clearly capture them
