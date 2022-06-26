#include<stdio.h>

int what_is_this()
{
  return system("cat flag");
}

char *__cdecl check_passwd(char *s)
{
  char dest[11]; // [esp+4h] [ebp-14h] BYREF
  unsigned __int8 v3; // [esp+Fh] [ebp-9h]

  v3 = strlen(s);
  if ( v3 <= 3u || v3 > 8u )
  {
    puts("Invalid Password");
    return (char *)fflush(stdout);
  }
  else
  {
    puts("Success");
    fflush(stdout);
    return strcpy(dest, s);
  }
}

int login()
{
  char buf[512]; // [esp+0h] [ebp-228h] BYREF
  char s[40]; // [esp+200h] [ebp-28h] BYREF

  memset(s, 0, 0x20u);
  memset(buf, 0, sizeof(buf));
  puts("Please input your username:");
  read(0, s, 0x19u);
  printf("Hello %s\n", s);
  puts("Please input your passwd:");
  read(0, buf, 0x199u);
  return check_passwd(buf);
}

int __cdecl main(int argc, const char **argv, const char **envp)
{
  int v4; // [esp+Ch] [ebp-Ch] BYREF

  setbuf(stdin, 0);
  setbuf(stdout, 0);
  setbuf(stderr, 0);
  puts("---------------------");
  puts("~~ Welcome to CTF! ~~");
  puts("       1.Login       ");
  puts("       2.Exit        ");
  puts("---------------------");
  printf("Your choice:");
  __isoc99_scanf("%d", &v4);
  if ( v4 == 1 )
  {
    login();
  }
  else
  {
    if ( v4 == 2 )
    {
      puts("Bye~");
      exit(0);
    }
    puts("Invalid Choice!");
  }
  return 0;
}
