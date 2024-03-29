# Lab 6: Environment Variable and Set-UID Program Lab

Objective: impart an understanding how environment variables influence program and system behaviors. The lab aims to elucidate the mechanisms through which environment variables affect program behaviors, enhancing students' comprehension and enabling them to develop more secure and robust software systems.

## Exercise 1: Manipulating Environment Variables

**A.1** 
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

Setting  enviroment variables
```bash
export MYVAR='Yachay'
env | grep MYVAR
```
Unsetting enviroment variables
```bash
unset MYVAR
env | grep MYVAR
```
![set unset env](/Lab6/exercise1/img/3.png)


