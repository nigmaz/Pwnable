#include<stdio.h>

int ignore()
{
  setvbuf(stdout, 0LL, 2, 0LL);
  setvbuf(stdin, 0LL, 2, 0LL);
  return setvbuf(stderr, 0LL, 2, 0LL);
}

int banner()
{
  puts("Do you know me?");
  return puts("Author: DucBT C/C++ v1.0");
}

int useme()
{
// code asm
}

int __cdecl main(int argc, const char **argv, const char **envp)
{
  ignore();
  banner(argc, argv);
  useme();
  return 1;
}
