#include<stdio.h>

int ignore()
{
  setvbuf(_bss_start, 0LL, 2, 0LL);
  setvbuf(stdin, 0LL, 2, 0LL);
  return setvbuf(stderr, 0LL, 2, 0LL);
}

unsigned __int64 crypto()
{
  unsigned int v0; // eax
  FILE *stream; // [rsp+8h] [rbp-48h]
  char format[16]; // [rsp+10h] [rbp-40h] BYREF // input
  char s[40]; // [rsp+20h] [rbp-30h] BYREF  // flag
  unsigned __int64 v5; // [rsp+48h] [rbp-8h] // canary

  v5 = __readfsqword(0x28u);
  v0 = time(0LL);
  srand(v0);
  rand();
  
  stream = fopen("flag.txt", "r");
  if ( !stream )
  {
    puts("No file flag.txt");
    exit(1);
  }
  fgets(s, 27, stream);
  puts("Input your name: ");
  __isoc99_scanf("%50s", format);
  printf(format);
  
  return __readfsqword(0x28u) ^ v5;
}

int __cdecl main(int argc, const char **argv, const char **envp)
{
  ignore(argc, argv, envp);
  crypto(argc, argv);
  return 0;
}

