#include<stdio.h>

__int64 vuln()
{
  char v1[32]; // [rsp+0h] [rbp-20h] BYREF

  printf("Say something : ");
  return gets(v1);
}

int __cdecl main(int argc, const char **argv, const char **envp)
{
  puts("Hello !!!!");
  vuln();
  return 0;
}
