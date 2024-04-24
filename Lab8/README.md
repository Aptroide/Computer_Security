# Lab 8: Packet Sniffing and Spoofing Lab

The objective of this lab is two-fold: learning to use the tools and understanding the technologies underlying these tools. For the second object, students will write simple sniffer and spoofing programs, and gain
an in-depth understanding of the technical aspects of these programs

## Environment Setup using Container

In this lab, we will use three machines that are connected to the same LAN. We can either use three VMs or three containers.  Image below depicts the lab environment setup using containers. We will do all the attacks on the attacker container, while using the other containers as the user machines.

![container_setup](/Lab8/container/1.png)

### Container Setup and Commands

To create our environmet we use `/Lab8/container/docker-compose.yml` and the commands:
```bash
docker-compose build  # Build the container image
docker-compose up     # Start the container
```
![container_setup](/Lab8/container/2.png)

All the containers will be running in the background. To run commands on a container, we often need to get a shell on that container. We do this by using:
```bash
dockps      # Alias for: docker ps --format "{{.ID}} {{.Names}}"
docksh <id> # Alias for: docker exec -it <id> /bin/bash
```
In our case we enter into `host B` shell:
![container_setup](/Lab8/container/3.png)

### About the Attacker Container

In this lab, we can either use the VM or the attacker container as the attacker machine. If you look at the Docker Compose file, you will see that the attacker container is configured differently from the other containers. Here are the differences:

- **Shared folder**: When we use the attacker container to launch attacks, we need to put the attacking code inside the attacker container. Code editing is more convenient inside the VM than in containers, because we can use our favorite editors. In order for the VM and container to share files, we have created a shared folder between the VM and the container using the Docker volumes. We will write our code in the `./volumes` folder (on the VM), so they can be used inside the containers

- **Host mode**: In this lab, the attacker needs to be able to sniff packets, but running sniffer programs inside a container has problems, because a container is effectively attached to a virtual switch, so it can only see its own traffic, and it is never going to see the packets among other containers. To solve this problem, we use the host mode for the attacker container. This allows the attacker container to see all the traffics. The following entry used on the attacker container:
  ```bash
  network_mode: host
  ```
  When a container is in the host mode, it sees all the host’s network interfaces, and it even has the same IP addresses as the host. Basically, it is put in the same network namespace as the host VM.

### Getting the network interface name

When we use the provided Compose file to create containers for this lab, a new network is created to connect the VM and the containers. The IP prefix for this network is `10.9.0.0/24`, which is specified in the `docker-compose.yml` file.

The  corresponding network interface name for our case is `br-a418d7bac199`.
```bash
[04/19/24]seed@VM:~/.../Labsetup$ ifconfig
br-a418d7bac199: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 10.9.0.1  netmask 255.255.255.0  broadcast 10.9.0.255
```


## Exercise 1: Using Scapy to Sniff and Spoof Packets

**Scapy can be used not only as a tool, but also as a building block to construct other sniffing and spoofing tools, i.e., we can integrate the Scapy functionalities into our own program. In this set of tasks, we will use Scapy for each task**

To use Scapy, we can write a Python program, and then execute this program using Python and root the root privilege because the privilege is required for spoofing packets.

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

We can also get into the interactive mode of Python and then run our program one line at a time at the Python prompt:
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

We will use Scapy as a building block to construct other tools. The objective of this task is to learn how to use Scapy to do packet sniffing in Python programs. To achive this we use `Lab8/exercise1/task1_1.py` file:
```python
#!/usr/bin/env python3
from scapy.all import *

def print_pkt(pkt):
	pkt.show()

pkt = sniff(iface='br-a418d7bac199', filter='icmp', prn=print_pkt)
```

#### Task 1.1A

In the above program, for each captured packet, the callback function print pkt() will be invoked; this function will print out some of the information about the packet.

##### With root privilege

We run `Lab8/exercise1/task1_1.py` with root privilege to demostrate that we can indeed capture packets.
```bash
sudo ./task1_1.py
```

As we can see on the image below, we succesfully get a packet by doing a ping from `hostA` (`10.9.0.5`)
![scapy](/Lab8/exercise1/img/3.png)
![scapy](/Lab8/exercise1/img/5.png)

##### Without root privilege
When we run `Lab8/exercise1/task1_1.py` without root privilege we can not recive a packet,because the privilege is required for spoofing packets.

![scapy](/Lab8/exercise1/img/4.png)

#### Task 1.1B
When we sniff packets, we are only interested certain types of packets. We can do that by setting filters in sniffing.

We work on the same file `Lab8/exercise1/task1_1B.py, but we use the acording filter for each task:

- To Capture only the ICMP packet.
  
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


- Capture any TCP packet that comes from a particular IP and with a destination port number 23.

  We use:
  ```python
  #!/usr/bin/env python3
  from scapy.all import *

  def print_pkt(pkt):
    pkt.show()

  filter_expr = 'tcp and host 10.9.0.5 and port 23'
  pkt = sniff(iface='br-a418d7bac199', filter=filter_expr, prn=print_pkt)
  ```
  To succesfully do get a packet, we need to send it using port 23, this port is the default port for telnet. So, in `hostB (10.9.0.6)` we run the following command (rigth window):
    ```python
  telnet 10.9.0.5
  ```
  This allow us to login into `hostA (10.9.0.5)` container via telnet, so our code can recieve some packets (left window).
  ![scapy](/Lab8/exercise1/img/6.png)

- Capture packets comes from or to go to a particular subnet. You can pick any subnet, such as `128.230.0.0/16`
  ```python
  #!/usr/bin/env python3
  from scapy.all import *

  def print_pkt(pkt):
    pkt.show()

  pkt = sniff(iface='br-a418d7bac199', filter='net 128.230.0.0/16', prn=print_pkt)
  ```
  We succesfully get a packet by doing a ping from `hostB (10.9.0.6)` to a host of the defined subnet (`128.230.0.15`)
    ```bash
  ping 128.230.0.15
    ```
    ![scapy](/Lab8/exercise1/img/7.png)

### Task 1.2 Spoofing ICMP Packets

As a packet spoofing tool, Scapy allows us to set the fields of IP packets to arbitrary values. The objective of this task is to spoof IP packets with an arbitrary source IP address. We will spoof ICMP echo request packets, and send them to another VM on the same network. We will use Wireshark to observe whether our
request will be accepted by the receiver. If it is accepted, an echo reply packet will be sent to the spoofed IP address. 

The `Lab8/exercise1/task1_2.py` file shows an example of how to spoof an ICMP packets.
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

We also need to setup Wireshark to recieve the packet from the host `1.2.3.4` and by the interface `enp0s3` as follows: 
![scapy](/Lab8/exercise1/img/8.png)

Now we run `Lab8/exercise1/task1_2.py` to send the packet and see it on Wireshark.
![scapy](/Lab8/exercise1/img/9.png)

### Task 1.3 Traceroute

The objective of this task is to use Scapy to estimate the distance, in terms of number of routers, between your VM and a selected destination.
The idea is quite straightforward: just send an packet (any type) to the destination, with its Time-To-Live (TTL) field set to 1 first. This packet will be dropped by the first router. While we increase our TTL field we will get the IP address of all the routers where our packet pass to finally get his final destination. To achive this we use `Lab8/exercise1/task1_3.py` file.
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
  ![scapy](/Lab8/exercise1/img/11.png)

- A non-existing host on the LAN
  ```bash
  ping  10.9.0.99
  ```
  ![scapy](/Lab8/exercise1/img/12.png)

  - An existing host on the Internet
  ```bash
  ping  8.8.8.8
  ```
  ![scapy](/Lab8/exercise1/img/13.png)