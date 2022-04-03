# FORMAT THREE

## About

This level advances from format2 and shows how to write more than 1 or 2 bytes of memory to the process. This also teaches you to carefully control what data is being written to the process memory.

This level is at /opt/protostar/bin/format3

## Source code

```C
#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>

int target;

void printbuffer(char *string)
{
  printf(string);
}

void vuln()
{
  char buffer[512];

  fgets(buffer, sizeof(buffer), stdin);

  printbuffer(buffer);
  
  if(target == 0x01025544) {
      printf("you have modified the target :)\n");
  } else {
      printf("target is %08x :(\n", target);
  }
}

int main(int argc, char **argv)
{
  vuln();
}
```

## Solutions

`FORMAT THREE` 


## Documents





