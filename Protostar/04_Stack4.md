# STACK FOUR

## About

Stack4 takes a look at overwriting saved EIP and standard buffer overflows.

This level is at /opt/protostar/bin/stack4

Hints

  * A variety of introductory papers into buffer overflows may help.
 
  * gdb lets you do “run < input”
 
 * EIP is not directly after the end of buffer, compiler padding can also increase the size.

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
  char buffer[64];

  gets(buffer);
}
```

## Solutions

`STACK FOUR` là thử thách sẽ bắt đầu xem xét việc nếu như buffer overflow không chỉ ghi đè giá trị của các biến trên STACK mà còn ghi đè những thứ khác có trên STACK.

Trước đó chúng ta sẽ xem lại cấu trúc Stack memory và code Assembly hàm main của chương trình qua gdb:

```
  |  high memory adddress
  | |====================| 
  | |   name-parameter   |  ^
  | |====================|  | buffer
  S |   return address   |  | fill
  t |====================|  | direction
  a |  base-pointer|'''''|  |
  c |==============|'''''|  |
  k |''''''''''''''''''''|  |
  | |'''''''buffer'''''''|  |
  | |''''''''''''''''''''|  |
  | |====================|  |
  | |                    |  |
  | |....................|
      low memory address
```

```Asm
root@protostar:/opt/protostar/bin# gdb -q ./stack4                                                      
Reading symbols from /opt/protostar/bin/stack4...done.                                                  
(gdb) set disassembly-flavor intel                                                                      
(gdb) disass main                                                                                       
Dump of assembler code for function main:                                                               
0x08048408 <main+0>:    push   ebp                                                                      
0x08048409 <main+1>:    mov    ebp,esp                                                                  
0x0804840b <main+3>:    and    esp,0xfffffff0                                                           
0x0804840e <main+6>:    sub    esp,0x50                                                                 
0x08048411 <main+9>:    lea    eax,[esp+0x10]                                                           
0x08048415 <main+13>:   mov    DWORD PTR [esp],eax                                                      
0x08048418 <main+16>:   call   0x804830c <gets@plt>                                                     
0x0804841d <main+21>:   leave                                                                           
0x0804841e <main+22>:   ret                                                                             
End of assembler dump.                                                                                  
(gdb) 
```



## Documents

<https://itandsecuritystuffs.wordpress.com/2014/03/18/understanding-buffer-overflows-attacks-part-1/>

<https://www.coengoedegebure.com/buffer-overflow-attacks-explained/>

<https://en.wikipedia.org/wiki/Endianness>


