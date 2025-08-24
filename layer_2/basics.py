from scapy.all import *

# a = Ether()
# a.show()

# b = IP(dst='10.12.52.220', src='10.12.59.249')
# b.show()

# c = ICMP()

# pkt = b/c

# pkt.show()

# response = sr1(IP(dst='8.8.8.8')/
#               UDP(dport=53)/
#               DNS(qd=DNSQR(qname="www.cisco.com",qtype='A')))

# response.show()


# send(pkt)

# print(req)


# send(IP(dst='10.12.59.249')/TCP(dport=12345, flags='SU'))

#fuzz will randomize the sport and dport


# send(IP(dst='10.12.52.220')/fuzz(TCP(dport=80)),loop=1)

packets = sniff(iface="wlan0")
packets.summary()