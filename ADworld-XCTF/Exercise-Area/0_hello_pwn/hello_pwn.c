#include<stdio.h>

__int64 sub_400686()
{
  system("cat flag.txt");
  return 0LL;
}

__int64 __fastcall main(int a1, char **a2, char **a3)
{
  alarm(0x3Cu);
  setbuf(stdout, 0LL);
  puts("~~ welcome to ctf ~~     ");
  puts("lets get helloworld for bof");
  read(0, &unk_601068, 0x10uLL);
  if ( dword_60106C == 0x6E756161 )	// 1853186401
    sub_400686();
  return 0LL;
}
