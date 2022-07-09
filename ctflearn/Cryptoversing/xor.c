#include<stdio.h>
#include<stdlib.c>

int __cdecl main(int argc, const char **argv, const char **envp)
{
  int i; // [rsp+4h] [rbp-CCh]
  int j; // [rsp+8h] [rbp-C8h]
  int k; // [rsp+Ch] [rbp-C4h]
  int v7[2]; // [rsp+18h] [rbp-B8h]
  int v8[2]; // [rsp+20h] [rbp-B0h]
  int v9[2]; // [rsp+28h] [rbp-A8h]
  char v10[64]; // [rsp+30h] [rbp-A0h] BYREF
  char s[72]; // [rsp+70h] [rbp-60h] BYREF
  unsigned __int64 v12; // [rsp+B8h] [rbp-18h]

  v12 = __readfsqword(0x28u);
  qmemcpy(v10, "h_bO}EcDOR+G)uh(jl,vL", 21);
  printf("[*] Hello! Welcome to our Program!\nEnter the password to contiune:  ");
  __isoc99_scanf("%s", s);
  v7[0] = 16;
  v7[1] = 24;
  v8[0] = strlen(s) >> 1;
  v8[1] = strlen(s);
  v9[0] = 0;
  v9[1] = strlen(s) >> 1;
  for ( i = 0; i <= 1; ++i )
  {
    for ( j = v9[i]; j < v8[i]; ++j )
      v10[j + 32] = v7[i] ^ s[j];
  }
  for ( k = 0; k < strlen(v10) - 1; ++k )
  {
    if ( v10[k + 32] != v10[k] )
    {
      puts("[-] Wrong Password");
      exit(0);
    }
  }
  puts("[+] Successful Login");
  return 0;
}
