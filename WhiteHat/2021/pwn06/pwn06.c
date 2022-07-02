#include<stdio.h>
char AZaz09[] = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";

int __cdecl main(int argc, const char **argv, const char **envp)
{
  size_t v3; // rax                                     // len(s)
  
  int i; // [rsp+Ch] [rbp-124h]				               4
  
  struct timeval tv; // [rsp+10h] [rbp-120h] BYREF	 3 	
  
  char s[128]; // [rsp+20h] [rbp-110h] BYREF		     2	// input
  char s2[136]; // [rsp+A0h] [rbp-90h] BYREF		     1	// password
  
  unsigned __int64 v9; // [rsp+128h] [rbp-8h]			      // canary
  v9 = __readfsqword(0x28u);

  setbuf(stdout, 0LL);
  setbuf(stdin, 0LL);
  gettimeofday(&tv, 0LL);

  srand(tv.tv_usec);				                            // srand time 
  for ( i = 0; i <= 126; ++i )
    s2[i] = AZaz09[rand() % 62];
  s2[128] = 0;
  
  puts("Smart Lock 4.0");
  puts("Enter password ...");
  
  while ( read(0, s, 0x200uLL) > 1 )
  {
    v3 = strlen(s);
    if ( !memcmp(s, s2, v3) )			                      // compare v3 value byte
    {
      puts("Access Granted");
      system("/bin/sh");
    }
    else
    {
      puts("Access Denied");
      printf(s);                                        // turn1 overwrite .text call system into puts GOT 
      puts(" is incorrect password");                   // jump to .text
    }
  }
  return 0;
}



