# FINAL ONE

## About

This level is a remote blind format string level. The ‘already written’ bytes can be variable, and is based upon the length of the IP address and port number.

When you are exploiting this and you don’t necessarily know your IP address and port number (proxy, NAT / DNAT, etc), you can determine that the string is properly aligned by seeing if it crashes or not when writing to an address you know is good.

Core files will be in /tmp.

This level is at /opt/protostar/bin/final1

## Source code

```C
#include "../common/common.c"

#include <syslog.h>

#define NAME "final1"
#define UID 0
#define GID 0
#define PORT 2994

char username[128];
char hostname[64];

void logit(char *pw)
{
  char buf[512];

  snprintf(buf, sizeof(buf), "Login from %s as [%s] with password [%s]\n", hostname, username, pw);

  syslog(LOG_USER|LOG_DEBUG, buf);
}

void trim(char *str)
{
  char *q;

  q = strchr(str, '\r');
  if(q) *q = 0;
  q = strchr(str, '\n');
  if(q) *q = 0;
}

void parser()
{
  char line[128];

  printf("[final1] $ ");

  while(fgets(line, sizeof(line)-1, stdin)) {
      trim(line);
      if(strncmp(line, "username ", 9) == 0) {
          strcpy(username, line+9);
      } else if(strncmp(line, "login ", 6) == 0) {
          if(username[0] == 0) {
              printf("invalid protocol\n");
          } else {
              logit(line + 6);
              printf("login failed\n");
          }
      }
      printf("[final1] $ ");
  }
}

void getipport()
{
  int l;
  struct sockaddr_in sin;

  l = sizeof(struct sockaddr_in);
  if(getpeername(0, &sin, &l) == -1) {
      err(1, "you don't exist");
  }

  sprintf(hostname, "%s:%d", inet_ntoa(sin.sin_addr), ntohs(sin.sin_port));
}

int main(int argc, char **argv, char **envp)
{
  int fd;
  char *username;

  /* Run the process as a daemon */
  background_process(NAME, UID, GID); 
  
  /* Wait for socket activity and return */
  fd = serve_forever(PORT);

  /* Set the client socket to STDIN, STDOUT, and STDERR */
  set_io(fd);

  getipport();
  parser();

}
```

## Solutions

`FINAL ONE` là khai thác `format string` và `remote`.

File final1.py

```

```

Khai thác

```

```

## Documents

[Final1](https://www.youtube.com/watch?v=MBz5C9Wa6KM)

[Medium](https://iphelix.medium.com/exploit-exercises-protostar-final-levels-72875b0c3387)

[pwntester](http://www.pwntester.com/blog/2013/12/26/protostar-final0-3-write-ups/)

[Reference](https://github.com/z3tta/Exploit-Exercises-Protostar)


