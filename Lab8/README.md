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

The  corresponding network interface name for our case is `10.9.0.1`.
```bash
[04/19/24]seed@VM:~/.../Labsetup$ ifconfig
br-a418d7bac199: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 10.9.0.1  netmask 255.255.255.0  broadcast 10.9.0.255
```


## Exercise 1: : Using Scapy to Sniff and Spoof Packets

