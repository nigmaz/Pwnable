#include<stdio.h>

int ignore()
{
  setvbuf(stdout, 0LL, 2, 0LL);
  setvbuf(stdin, 0LL, 2, 0LL);
  return setvbuf(stderr, 0LL, 2, 0LL);
}

int bash()
{
  return system("/bin/sh");
}

__int64 member()
{
  char v1[64]; // [rsp+0h] [rbp-40h] BYREF

  puts("Ting ting!");
  puts("Baby gets my gun!");
  return gets(v1);
}

int __cdecl main(int argc, const char **argv, const char **envp)
{
  ignore(argc, argv, envp);
  member(argc, argv);
  return 0;
}
