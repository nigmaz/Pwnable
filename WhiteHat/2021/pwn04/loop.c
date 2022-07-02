#include<stdio.h>

int func01()
{
  return printf("Welcome to VietNam!!!\n");
}

char *__fastcall func02(char *a1, int a2)
{
  printf("What's your name? ");
  return fgets(a1, a2, stdin);
}

__int64 __fastcall func03(const char *a1)
{
  printf("Hello ");
  printf(a1, 0LL);
  puts("\nWe will suggest you some interesting places in Vietnam");
  puts("[+] Ha Long bay.");
  puts("[+] Phu Quoc island.");
  puts("[+] Kong island.");
  puts("[+] Hoan Kiem lake.");
  puts("[+] Sapa.");
  puts("[+] ...");
  puts("Wish you have great moments in Vietnam!");
  return 0LL;
}

int __cdecl main(int argc, const char **argv, const char **envp)
{
  char v4[72]; // [rsp+10h] [rbp-50h] BYREF
  unsigned __int64 v5; // [rsp+58h] [rbp-8h]

  v5 = __readfsqword(0x28u);
  setvbuf(stdin, 0LL, 2, 0LL);
  setvbuf(stdout, 0LL, 2, 0LL);
  setvbuf(stderr, 0LL, 2, 0LL);
  func01();
  func02(v4, 64);
  func03(v4);
  return 0;
}



