#!/usr/bin/env python3
from scapy.all import *

def print_pkt(pkt):
	pkt.show()

## 1.1B
# Capture only the ICMP packet
#pkt = sniff(iface='br-a418d7bac199', filter='icmp', prn=print_pkt)

# Capture any TCP packet that comes from a particular IP 
# and with a destination port number 23.
filter_expr = 'tcp and host 10.9.0.5 and port 23'
#pkt = sniff(iface='br-a418d7bac199', filter=filter_expr, prn=print_pkt)

# Capture packets comes from or to go to a particular subnet
pkt = sniff(iface='br-a418d7bac199', filter='net 128.230.0.0/16', prn=print_pkt)
