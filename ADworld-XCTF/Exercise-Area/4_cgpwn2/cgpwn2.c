#include<stdio.h>
int name;

int pwn()
{
  return system("echo hehehe");
}

char *hello()
{
  __int16 *p_s; // eax
  char v1; // bl
  unsigned int v2; // ecx
  __int16 *v3; // eax
  __int16 s; // [esp+12h] [ebp-26h] BYREF
  int v6; // [esp+14h] [ebp-24h] BYREF

  p_s = &s;
  v1 = 30;
  if ( ((unsigned __int8)&s & 2) != 0 )
  {
    s = 0;
    p_s = (__int16 *)&v6;
    v1 = 28;
  }
  v2 = 0;
  do
  {
    *(_DWORD *)&p_s[v2 / 2] = 0;
    v2 += 4;
  }
  while ( v2 < (v1 & 0x1Cu) );
  v3 = &p_s[v2 / 2];
  if ( (v1 & 2) != 0 )
    *v3 = 0;
  puts("please tell me your name");
  fgets(name, 50, stdin); 	// no cho phep luu /bin/sh vao roi goi lai de nhan shell voi bien toan cuc name 
  puts("hello,you can leave some message here:");
  return gets((char *)&s);	// tra ve dia chi bien toan cuc luu shell vao .bss roi goi dia chi
}

int __cdecl main(int argc, const char **argv, const char **envp)
{
  setbuf(stdin, 0);
  setbuf(stdout, 0);
  setbuf(stderr, 0);
  
  hello();
  
  puts("thank you");
  return 0;
}


