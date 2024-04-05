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

To show how this works, we have `/Lab7/exercise1/call_shellcode.c` file, that togheter with `/Lab7/exercise1/Makefile` creates two copies of shellcode, one is 32-bit and the other is 64-bit.

By writing `make`, we are using:
```bash
gcc -m32 -z execstack -o a32.out call_shellcode.c
gcc -z execstack -o a64.out call_shellcode.c
```
![make](/Lab7/exercise1/img/1.png)

We can see on the image that both binaries run without any problem despite we are working on a 64-bit VM.
Modern linux OS include compatibility layers (such as the ia32-libs package) that allow them to run 32-bit binaries. This is accomplished through the use of system libraries that can handle the translation from 32-bit to 64-bit system calls.


If we make `/Lab7/exercise1/a32.out` and `/Lab7/exercise1/a64.out` a root-owned Set-UID programs, we can get into the root shell.

![make](/Lab7/exercise1/img/2.png)
