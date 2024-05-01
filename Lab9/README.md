
# Lab 9: ARP Cache Poisoning Attack Lab

The Address Resolution Protocol (ARP) serves to discover the link layer address (such as MAC address) corresponding to a given IP address. It lacks security measures, making it vulnerable to ARP cache poisoning attacks. In such attacks, attackers manipulate ARP caches to forge IP-to-MAC mappings, redirecting victim packets to a fraudulent MAC address and potentially enabling man-in-the-middle attacks.

The primary objective of the lab is to provide students with practical exposure to ARP cache poisoning attacks, enabling them to understand the ramifications of such vulnerabilities. Specifically, students engage in launching man-in-the-middle attacks by exploiting ARP vulnerabilities, allowing interception and modification of packets between two victim nodes, denoted as A and B. Additionally, the lab aims to reinforce students' proficiency in essential network security skills, particularly packet sniffing and spoofing. These skills are foundational for understanding various network attack and defense strategies.

## Environment Setup using Container

In this lab, we need several machines connected to the same LAN. The image below depicts the lab environment setup using containers. 

![container_setup](/Lab9/container/1.png)

### Container Setup and Commands

To create our environment, we use `/Lab9/container/docker-compose.yml` and the commands:
```bash
docker-compose build  # Build the container image
docker-compose up     # Start the container
```
![container_setup](/Lab9/container/2.png)

All the containers will run in the background. To run commands on a container, we often need to get a shell on that container. We do this by using:
```bash
dockps      # Alias for: docker ps --format "{{.ID}} {{.Names}}"
docksh <id> # Alias for: docker exec -it <id> /bin/bash
```
The following example shows how to get a shell inside Host A:
```bash
[05/01/24]seed@VM:~/.../Lab9$ dockps
8dababab2b99  B-10.9.0.6
7cb568e00598  A-10.9.0.5
4228c9280821  M-10.9.0.105
[05/01/24]seed@VM:~/.../Lab9$ docksh 7c
root@7cb568e00598:/# 
```
![container_setup](/Lab9/container/3.png)

### About the Attacker Container

In this lab, we can use either the VM or the attacker container as the attacker machine. On the `/Lab9/container/docker-compose.yml` file, we see that the attacker container is configured differently from the other containers. Here are the differences:

- **Shared folder**: A shared folder between the VM and the container, created using Docker volumes, facilitates file sharing for attack execution.

- **Privileged mode**: To be able to modify kernel parameters at runtime (using sysctl), such as enabling IP forwarding, a container needs to be privileged. This is achieved by including the following entry in the Docker Compose file for the container.
  ```bash
  privileged: true
  ```

### Packet Sniffing

Packet sniffing is essential in this lab for observing network traffic and diagnosing issues. Several methods for packet sniffing are available:

1. Using tcpdump on Containers:
   - Execute the following command to sniff packets on a specific interface (e.g., eth0):
     ```
     tcpdump -i eth0 -n
     ```
   - Note: Within containers, packet sniffing is limited to packets going in and out of the container. Host mode can enable sniffing of other containers' packets.

2. Using tcpdump on the VM:
   - Running tcpdump on the VM allows sniffing of all packets exchanged among containers.
   - Interface names differ between VM and containers. Use the `ip address` command to retrieve the interface name.

3. Using Wireshark on the VM:
   - Wireshark offers a graphical interface for packet sniffing.
   - Select the desired interface for sniffing.

By employing these methods, we can monitor network traffic effectively, aiding in understanding and troubleshooting ARP cache poisoning attacks and network vulnerabilities.






## Exercise 1: Launching ICMP Redirect Attack

### Turning Off contermeasure

In the Ubuntu operating system, there is a countermeasure against the ICMP redirect attack. In the Compose file, we have already turned off the countermeasure by configuring the victim container to accept ICMP redirect messages.

```bash
# In docker-compose.yml
net.ipv4.conf.all.accept_redirects=1
# To turn the protection on, set its value to 0
net.ipv4.conf.all.accept_redirects=0
```

### Code skeleton

A code skeleton is provided in `Lab9/exercise1/skeleton.py`.



**Scapy can be used not only as a tool but also as a building block to construct other sniffing and spoofing tools, i.e., we can integrate the Scapy functionalities into our own programs. In this set of tasks, we will use Scapy for each task.**

To use Scapy, we can write a Python program and then execute this program using Python with root privileges because such privileges are required for spoofing packets.

```python
#!/usr/bin/env python3
from scapy.all import *

a = IP()
a.show()
```
**In order to run all the files for this lab, we first need to change the permissions of the scripts.**

```bash
chmod a+x <file_name>
```

```bash
[04/24/24]seed@VM:~/.../ex1$ escapy.py 
###[ IP ]### 
  version   = 4
  ihl       = None
  tos       = 0x0
  len       = None
  id        = 1
  flags     = 
  frag      = 0
  ttl       = 64
  proto     = hopopt
  chksum    = None
  src       = 127.0.0.1
  dst       = 127.0.0.1
  \options   \
```
![scapy](/Lab8/exercise1/img/1.png)

We can also enter the interactive mode of Python and then run our program one line at a time at the Python prompt:
```bash
[04/24/24]seed@VM:~/.../ex1$ python3
>>> from scapy.all import *
>>> a = IP()
>>> a.show()
###[ IP ]### 
  version   = 4
  ihl       = None
  tos       = 0x0
  len       = None
  id        = 1
  ...
```
![scapy](/Lab8/exercise1/img/2.png)

### Task 1.1 Sniffing Packets

We will use Scapy as a building block to construct other tools. The objective of this task is to learn how to use Scapy to perform packet sniffing in Python programs. To achieve this, we use the `Lab8/exercise1/task1_1.py` file:
```python
#!/usr/bin/env python3
from scapy.all import *

def print_pkt(pkt):
    pkt.show()

pkt = sniff(iface='br-a418d7bac199', filter='icmp', prn=print_pkt)
```

#### Task 1.1A

The goal of this task is to utilize Scapy to construct packet sniffing tools. For each captured packet, the callback function `print_pkt()` is invoked, displaying packet details.

##### With root privileges

Running `Lab8/exercise1/task1_1.py` with root privileges allows us to capture ICMP packets effectively from `hostA` (`10.9.0.5`):
```bash
sudo ./task1_1.py
```

As we can see in the images below, we successfully captured a packet by performing a ping from `hostA` (`10.9.0.5`):
![scapy](/Lab8/exercise1/img/3.png)
![scapy](/Lab8/exercise1/img/5.png)

##### Without root privileges

Lacking root privileges, the script fails to capture packets, highlighting the necessity of appropriate permissions for packet operations.

![scapy](/Lab8/exercise1/img/4.png)


#### Task 1.1B
When we sniff packets, we are interested in only certain types of packets. We can specify this by setting filters in sniffing.

We work on the same file `Lab8/exercise1/task1_1B.py`, but we use the appropriate filter for each task:

- **To Capture Only the ICMP Packet:**

  We use:
  ```python
  #!/usr/bin/env python3
  from scapy.all import *

  def print_pkt(pkt):
    pkt.show()

  pkt = sniff(iface='br-a418d7bac199', filter='icmp', prn=print_pkt)
  ```
  And a ping from `hostA` (`10.9.0.5`)
  ![scapy](/Lab8/exercise1/img/3.png)

- **Capture Any TCP Packet That Comes from a Particular IP and with a Destination Port Number 23:**

  We use:
  ```python
  #!/usr/bin/env python3
  from scapy.all import *

  def print_pkt(pkt):
    pkt.show()

  filter_expr = 'tcp and host 10.9.0.5 and port 23'
  pkt = sniff(iface='br-a418d7bac199', filter=filter_expr, prn=print_pkt)
  ```
  To successfully capture a packet, we need to send it using port 23, which is the default port for Telnet. Therefore, on `hostB (10.9.0.6)`, we run the following command (right window):
    ```bash
  telnet 10.9.0.5
  ```
  This allows us to log into `hostA (10.9.0.5)` container via Telnet, so our code can receive some packets (left window).
  ![scapy](/Lab8/exercise1/img/6.png)

- **Capture Packets That Come From or Go to a Particular Subnet:**

  You can pick any subnet, such as `128.230.0.0/16`
  ```python
  #!/usr/bin/env python3
  from scapy.all import *

  def print_pkt(pkt):
    pkt.show()

  pkt = sniff(iface='br-a418d7bac199', filter='net 128.230.0.0/16', prn=print_pkt)
  ```
  We successfully capture a packet by doing a ping from `hostB (10.9.0.6)` to a host in the defined subnet (`128.230.0.15`)
    ```bash
  ping 128.230.0.15
    ```
    ![scapy](/Lab8/exercise1/img/7.png)


### Task 1.2 Spoofing ICMP Packets

As a packet spoofing tool, Scapy enables us to set the fields of IP packets to arbitrary values. The objective of this task is to spoof IP packets with an arbitrary source IP address. We will spoof ICMP echo request packets and send them to another VM on the same network. We will use Wireshark to observe whether our request is accepted by the receiver. If accepted, an echo reply packet will be sent to the spoofed IP address.

The `Lab8/exercise1/task1_2.py` file provides an example of how to spoof ICMP packets.
```python
#!/usr/bin/env python3
from scapy.all import *

a = IP()
a.dst = '1.2.3.4'
b = ICMP()
p = a/b

ls(a)
send(p)
```

We also need to set up Wireshark to receive the packet from the host `1.2.3.4` and by the interface `enp0s3` as follows: 
![scapy](/Lab8/exercise1/img/8.png)

Now, we run `Lab8/exercise1/task1_2.py` to send the packet and observe it on Wireshark.
![scapy](/Lab8/exercise1/img/9.png)

### Task 1.3 Traceroute

The objective of this task is to use Scapy to estimate the number of routers between your VM and a selected destination. The idea is straightforward: send a packet (any type) to the destination with its Time-To-Live (TTL) field initially set to 1. This packet will be dropped by the first router. As we increase the TTL, we will receive the IP addresses of all the routers through which our packet passes until it reaches its final destination. To achieve this, we use the `Lab8/exercise1/task1_3.py` file.
```python
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
```

![scapy](/Lab8/exercise1/img/10.png)

### Task 1.4 Sniffing and-then Spoofing

In this task, we will combine the sniffing and spoofing techniques to implement the following sniff-andthen-spoof program. We need two machines on the same LAN: the `VM (10.9.0.1)` and the `hostB (10.9.0.6)`. From the `hostB`, we ping an IP X. This will generate an ICMP echo request packet. Your sniff-and-then-spoof program runs on the `VM`, which monitors the LAN through packet sniffing. Whenever it sees an ICMP echo request, regardless of what the target IP address is, your program should immediately send out an echo reply using the packet spoofing technique. Therefore, regardless of whether machine X is alive or not, the ping program will always receive a reply, indicating that X is alive. 
```python
#!/usr/bin/env python3
import sys
import os
from scapy.all import *


def spoof_pkt(pkt):
    # sniff and print out icmp echo request packet
    if ICMP in pkt and pkt[ICMP].type == 8:
        print("Original Packet.........")
        print("Source IP : ", pkt[IP].src)
        print("Destination IP :", pkt[IP].dst)

        # spoof an icmp echo reply packet
        # swap srcip and dstip
        ip = IP(src=pkt[IP].dst, dst=pkt[IP].src, ihl=pkt[IP].ihl)
        icmp = ICMP(type=0, id=pkt[ICMP].id, seq=pkt[ICMP].seq)
        data = pkt[Raw].load
        newpkt = ip/icmp/data

        print("Spoofed Packet.........")
        print("Source IP : ", newpkt[IP].src)
        print("Destination IP :", newpkt[IP].dst)

        send(newpkt, verbose=0)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: sudo {} host_ip\n".format(
            sys.argv[0]))
        exit(1)

    host_ip = sys.argv[1]
    filter = 'icmp and host '+ host_ip
    print("filter: {}\n".format(filter))

    pkt = sniff(filter=filter, prn=spoof_pkt)
```

To use `Lab8/exercise1/task1_4.py` file, we need to run it like:
```bash
./task1_4/py <Host IP>
```

The snecarios are:

- A non-existing host on the Internet
  ```bash
  ping 1.2.3.4
  ```
  If the IP address exists in the LAN, ARP will resolve it to a valid MAC address, and the data packets can reach their destination. This means that spoofed packets with a source IP of an existing local host will reach the target because the ARP protocol can successfully map the IP to a MAC address.

  We observe that a ping request is sent to IP address `1.2.3.4` which doesn't exist in the local network. The left terminal shows the `Lab8/exercise1/task1_4.py` script capturing this ICMP request and sending a spoofed ICMP reply, making it appear as though `1.2.3.4` is an active host. The right terminal confirms this by showing that ping receives responses, even though there is no such host in reality.

  ![scapy](/Lab8/exercise1/img/11.png)

- A non-existing host on the LAN
  ```bash
  ping  10.9.0.99
  ```
  If the IP address does not exist on the local network, ARP requests for this IP will not be answered, and the network stack will eventually give up, resulting in a **"Destination Host Unreachable"** error at the IP layer, despite any spoofed ICMP replies. This error occurs because the data link layer (Ethernet) cannot proceed without a MAC address, even if the network layer (IP) packets are being spoofed.

  Depicts an attempt to ping `10.9.0.99`, a non-existent local host. Again, the left terminal demonstrates the capture of this ICMP request by the `Lab8/exercise1/task1_4.py` script and the sending of a spoofed reply. The right terminal, however, shows **"Destination Host Unreachable"** messages, which indicate that, despite the spoofing attempt, the network layer (IP) is reporting that the subnet can't be reached. This is likely due to ARP not being able to resolve the non-existent IP to a valid MAC address in the local network.
  ![scapy](/Lab8/exercise1/img/12.png)

  - An existing host on the Internet
  ```bash
  ping  8.8.8.8
  ```
  The `Lab8/exercise1/task1_4.py` script on the left captures  requests and sends spoofed replies, as shown in the terminal output. However, the right terminal shows actual ping responses from `8.8.8.8`, including the time taken for the round trip. Since `8.8.8.8` is outside the local network, ARP does not play a role here; instead, routing takes place, and the spoofed responses from the script do not interfere with the actual responses coming from the Google server.
  ![scapy](/Lab8/exercise1/img/13.png)

In conclusion, the observations from the tasks demonstrate that while spoofing can manipulate responses within a local network segment, it is limited by ARP protocol behavior and routing mechanisms outside the local network. Spoofing can create the illusion of a host's presence on a local network by replying to ARP requests and ICMP pings but cannot influence traffic once it leaves the local network for an external destination, such as the internet.






