from scapy.all import *

dest = input("Enter Target: ")

pkt = IP(dst = dest)/UDP(sport = random.randint(1,65535),dport = random.randint(1,65535))

for i in range(1,10):
    send(pkt)
    print(f"sent {i} packet")