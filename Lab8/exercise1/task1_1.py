#!/usr/bin/env python3
from scapy.all import *

def print_pkt(pkt):
	pkt.show()

pkt = sniff(iface='br-a418d7bac199', filter='icmp', prn=print_pkt)
