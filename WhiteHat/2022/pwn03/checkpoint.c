#include<stdio.h>

int ignore()
{
  setvbuf(stdout, 0LL, 2, 0LL);
  setvbuf(stdin, 0LL, 2, 0LL);
  return setvbuf(stderr, 0LL, 2, 0LL);
}

int checkpoint()
{
  unsigned int v0; // eax
  char v2[24]; // [rsp+0h] [rbp-20h] BYREF
  unsigned int v3; // [rsp+18h] [rbp-8h]
  int v4; // [rsp+1Ch] [rbp-4h]

  v4 = 0;
  v0 = time(0LL);
  srand(v0);
  v3 = rand() % 99;
  puts("Do you want check point of exam?");
  puts("Find them exam: ");
  gets(v2);
  if ( v4 == 100 ) // v4 = 0x64
  {
    puts("Congratulation: 100 point! You done!");
    return system("cat flag.txt");
  }
  else
  {
    printf("You have %d point < 100\n", v3);
    return puts("Noob! :p");
  }
}

int __cdecl main(int argc, const char **argv, const char **envp)
{
  ignore();
  checkpoint(argc, argv);
  return 1;
}
