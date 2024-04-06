# Lab 7: Buffer Overflow Attack Lab (Set-UID Version)

Objective: develop a scheme to exploit the vulnerability and finally gain the root privilege. In addition to the attacks, students will be guided to walk through several protection schemes that have been implemented in the operating system to counter against buffer-overflow attacks. Students need to evaluate whether the schemes work or not and explain why.

## Turning Off Countermeasures

Modern operating systems have implemented several security mechanisms to make the buffer-overflow attack difficult. To simplify our attacks, we need to disable them first. Later on, we will enable them and see whether our attack can still be successful or not.

### Address Space Randomization

Ubuntu and several other Linux-based systems uses address space randomization to randomize the starting address of heap and stack. This makes guessing the exact addresses difficult; guessing addresses is one of the critical steps of buffer-overflow attacks. This feature can be disabled using the following command:
```bash
sudo sysctl -w kernel.randomize_va_space=0
```

### Configuring /bin/sh

In the recent versions of Ubuntu OS, the `/bin/sh` symbolic link points to the `/bin/dash` shell. The dash program, as well as bash, has implemented a security countermeasure that prevents itself from being executed in a Set-UID process. Basically, if they detect that they are executed in a Set-UID process, they will immediately change the effective user ID to the process’s real user ID, essentially dropping the privilege.

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


If we make `/Lab7/exercise1/a32.out` and `/Lab7/exercise1/a64.out` root-owned Set-UID programs, we can obtain a root shell.

![make](/Lab7/exercise1/img/2.png)


## Exercise 2: Understanding the Vulnerable Program

The vulnerable program used in this lab is `/Lab7/exercise2/stack.c`. This program has a buffer-overflow vulnerability, and your job is to exploit this vulnerability and gain the root privilege. 

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

- `stack-LX`: 32-bit and 64 bit vulnerable programs for diferents levels (X).
- `stack-X-dbg`: 32-bit and 64 bit vulnerable program with debugging information added to the  for diferents levels (X).

## Exercise 3: Launching Attack on 32-bit Program (Level 1)


### Investigation

To exploit the buffer-overflow vulnerability in the target program, the most important thing to know is the distance between the buffer’s starting position and the place where the return-address is stored. We will use a debugging method to find it out. Since we have the source code of the target program, we can compile it with the debugging flag turned on. That will make it more convenient to debug.

```bash
[04/06/24]seed@VM:~/.../Lab7$ gdb stack-L1-dbg 
gdb-peda$ b bof
Breakpoint 1 at 0x80484c1: file stack.c, line 18.
gdb-peda$ run
...
Breakpoint 1, bof (str=0xbfffeb57 "\bB\003") at stack.c:18
18	    strcpy(buffer, str); 
...
gdb-peda$ p/x &buffer
$1 = 0xbfffeacc
gdb-peda$ p/x $ebp
$2 = 0xbfffeb38
```

Now we know that:
- buffer = 0xbfffeacc
- ebp = 0xbfffeb38
- L = 4
- offset = ebp - buffer + L
- ret = buffer + offset + 100


# Calculate the offset to place the return address right after the buffer
offset = 0xbfffeb38 - 0xbfffeacc + L # The size of the buffer in the vulnerable program
# Use a debugger to find the correct return address.
ret = 0xbfffeacc + offset + 100 