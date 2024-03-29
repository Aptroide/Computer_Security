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

Comment out the `printenv()` statement in the **child process** case, and uncomment the `printenv()` statement in the **parent process** case.

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