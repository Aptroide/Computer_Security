#!/usr/bin/env python3

from scapy.all import *

# Destination IP address
destination = '8.8.8.8'

# Maximum number of routers to try
max_hops = 30

# Iterate over TTL values from start_ttl to max_hops
for ttl in range(1, max_hops + 1):
    a = IP(dst=destination, ttl=ttl)
    b = ICMP()
    
    # Send the packet and wait for a reply
    reply = sr1(a/b, verbose=0, timeout=2)
    
    # Handle no reply
    if reply is None:
        print(f"{ttl}: No reply")
        continue
    
    # Print the source of the reply
    print(f"{ttl}: Source: {reply.src}")
    
    # If the reply is an echo-reply, break the loop as the destination was reached
    if reply.type == 0:
        print("Reached the destination.")
        break

