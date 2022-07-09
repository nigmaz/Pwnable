#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>
#include <unistd.h>
#include <sys/types.h>
 
#define BUFFER 512
 
struct Init
{
  char username[128];
  uid_t uid;
  pid_t pid;  
   
};
 
void cpstr(char *dst, const char *src)
{
  for(; *src; src++, dst++)
    {
      *dst = *src;
    }
  *dst = 0;
}
void chomp(char *buff)
{
  for(; *buff; buff++)
    {
      if(*buff == '\n' || *buff == '\r' || *buff == '\t')
        {
          *buff = 0;
          break;
        }
    }
}
struct Init Init(char *filename)
{
   
  FILE *file;
  struct Init init;
  char buff[BUFFER+1];  
   
   
  if((file = fopen(filename, "r")) == NULL)
    {
      perror("[-] fopen ");
      exit(0);
    }
   
  memset(&init, 0, sizeof(struct Init));
   
  init.pid = getpid();
  init.uid = getuid();
   
  while(fgets(buff, BUFFER, file) != NULL)
    {
      chomp(buff);
      if(strncmp(buff, "USERNAME=", 9) == 0)
        {
          cpstr(init.username, buff+9);
        }
    }
  fclose(file);
  return init;
}
int main(int argc, char **argv)
{
  struct Init init;
  if(argc != 2)
    {
      printf("Usage : %s <config_file>\n", argv[0]);
      exit(0);
    }
  init = Init(argv[1]);
  printf("[+] Runing the program with username %s, uid %d and pid %d.\n", init.username, init.uid, init.pid);
   
  return 0;
}

// 	ssh -p 2222 app-systeme-ch10@challenge02.root-me.org 


