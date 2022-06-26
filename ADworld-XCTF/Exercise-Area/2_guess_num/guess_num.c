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
// dung ida ms phan tich dc
