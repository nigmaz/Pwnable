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

Chúng ta quan tâm tới con trỏ v4 được cấp phát động, `v4 = 68` và `v4[1] = 85` và tương ứng với `secret[0]` và `secret[1]` được in ra là địa chỉ của `v4` và `v4[0]`.




