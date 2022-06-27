#include<stdio.h>

// option: 1
unsigned __int64 sub_400960()
{
  char buf[136]; // [rsp+0h] [rbp-90h] BYREF
  unsigned __int64 v2; // [rsp+88h] [rbp-8h]

  v2 = __readfsqword(0x28u);
  memset(buf, 0, 0x80uLL);
  read(0, buf, 0x100uLL);
  printf("-> %s\n", buf);
  return __readfsqword(0x28u) ^ v2;
}

// option: 2
unsigned __int64 sub_4008EB()
{
  char buf[136]; // [rsp+0h] [rbp-90h] BYREF
  unsigned __int64 v2; // [rsp+88h] [rbp-8h]

  v2 = __readfsqword(0x28u);
  memset(buf, 0, 0x80uLL);
  read(0, buf, 0x7FuLL);
  printf(buf);
  return __readfsqword(0x28u) ^ v2;
}

int sub_4009DA()
{
  puts("1. Stack Bufferoverflow Bug ");
  puts("2. Format String Bug ");
  return puts("3. Exit the battle ");
}

// alarm
unsigned int sub_4009FF()
{
  setvbuf(stdin, 0LL, 1, 0LL);
  setvbuf(stdout, 0LL, 2, 0LL);
  return alarm(0x14u);
}

void __fastcall __noreturn main(int a1, char **a2, char **a3)
{
  int v3; // [rsp+24h] [rbp-Ch] BYREF
  unsigned __int64 v4; // [rsp+28h] [rbp-8h]

  v4 = __readfsqword(0x28u);
  sub_4009FF();     // chi xet thoi gian nhap
  puts("Welcome to the battle ! ");
  puts("[Great Fairy] level pwned ");
  puts("Select your weapon ");
  while ( 1 )
  {
    while ( 1 )
    {
      sub_4009DA();
      __isoc99_scanf("%d", &v3);
      if ( v3 != 2 )
        break;
      sub_4008EB();
    }
    if ( v3 == 3 )
    {
      puts("Bye ");
      exit(0);
    }
    if ( v3 == 1 )
      sub_400960();
    else
      puts("Wrong!");
  }
}

// 1 so ham 

int sub_4008DA()
{
  return system("/bin/cat ./flag");
}



