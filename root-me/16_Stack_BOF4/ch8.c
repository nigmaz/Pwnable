#include <stdio.h>
#include <stdlib.h>
#include <dirent.h>
#include <string.h>
 
struct EnvInfo
{
  char home[128];
  char username[128];
  char shell[128];  
  char path[128];  
};
 
 
struct EnvInfo GetEnv(void)
{
  struct EnvInfo env;
  char *ptr;
   
  if((ptr = getenv("HOME")) == NULL)
    {
      printf("[-] Can't find HOME.\n");
      exit(0);
    }
  strcpy(env.home, ptr);
  if((ptr = getenv("USERNAME")) == NULL)
    {
      printf("[-] Can't find USERNAME.\n");
      exit(0);
    }
  strcpy(env.username, ptr);
  if((ptr = getenv("SHELL")) == NULL)
    {
      printf("[-] Can't find SHELL.\n");
      exit(0);
    }
  strcpy(env.shell, ptr);
  if((ptr = getenv("PATH")) == NULL)
    {
      printf("[-] Can't find PATH.\n");
      exit(0);
    }
  strcpy(env.path, ptr);
  return env;
}
 
int main(void)
{
  struct EnvInfo env;
   
  printf("[+] Getting env...\n");
  env = GetEnv();
   
  printf("HOME     = %s\n", env.home);
  printf("USERNAME = %s\n", env.username);
  printf("SHELL    = %s\n", env.shell);
  printf("PATH     = %s\n", env.path);
   
  return 0;  
}

// ssh -p 2222 app-systeme-ch8@challenge02.root-me.org


