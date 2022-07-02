#include<stdio.h>

int __cdecl execute(int a1, int a2)
{
  void *v2; // esp
  int v3; // eax
  _DWORD v5[3]; // [esp+0h] [ebp-28h] BYREF
  int (*v6)(void); // [esp+Ch] [ebp-1Ch]
  int v7; // [esp+10h] [ebp-18h]
  unsigned int v8; // [esp+14h] [ebp-14h]
  int v9; // [esp+18h] [ebp-10h]
  unsigned int i; // [esp+1Ch] [ebp-Ch]

  if ( !a1 || !a2 )
    exit(1);
  v8 = 2 * a2;
  v7 = 2 * a2;
  v2 = alloca(16 * ((2 * a2 + 16) / 0x10u));
  v6 = (int (*)(void))v5;
  v9 = 0;
  for ( i = 0; v8 > i; ++i )
  {
    if ( (int)i % 4 > 1 )
    {
      *((_BYTE *)v6 + i) = -112;
    }
    else
    {
      v3 = v9++;
      *((_BYTE *)v6 + i) = *(_BYTE *)(v3 + a1);
    }
  }
  *((_BYTE *)v6 + v8) = -61;
  v5[2] = v6;
  return v6();
}

int __cdecl main(int argc, const char **argv, const char **envp)
{
  char v4[1000]; // [esp+1h] [ebp-3F5h] BYREF
  _DWORD v5[3]; // [esp+3E9h] [ebp-Dh]

  *(_DWORD *)((char *)&v5[1] + 1) = &argc;
  setbuf(stdout, 0);
  LOBYTE(v5[1]) = 0;
  puts("Give me code to run:");
  v5[0] = (unsigned __int8)fgetc(stdin);
  while ( LOBYTE(v5[0]) != 10 && *(_DWORD *)((char *)v5 + 1) <= 0x3E7u )
  {
    v4[*(_DWORD *)((char *)v5 + 1)] = v5[0];
    LOBYTE(v5[0]) = fgetc(stdin);
    ++*(_DWORD *)((char *)v5 + 1);
  }
  if ( (v5[0] & 0x100) != 0 )
    v4[(*(_DWORD *)((char *)v5 + 1))++] = -112;
  execute(v4, *(_DWORD *)((char *)v5 + 1));
  return 0;
}
