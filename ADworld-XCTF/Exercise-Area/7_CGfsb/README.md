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

