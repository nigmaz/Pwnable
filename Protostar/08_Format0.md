# FORMAT ZERO

## About

This level introduces format strings, and how attacker supplied format strings can modify the execution flow of programs.

Hints

  * This level should be done in less than 10 bytes of input.
  
  * “Exploiting format string vulnerabilities”

This level is at /opt/protostar/bin/format0

## Source code

```C
#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>

void vuln(char *string)
{
  volatile int target;
  char buffer[64];

  target = 0;

  sprintf(buffer, string);
  
  if(target == 0xdeadbeef) {
      printf("you have hit the target correctly :)\n");
  }
}

int main(int argc, char **argv)
{
  vuln(argv[1]);
}
```

## Solutions

`FORMAT ZERO` 


## Documents





