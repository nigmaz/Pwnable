# XCTF - PWN Exercise - string

Kiếm tra các flag secure trước.

```
l1j9m4 in ~/0_PWNable/ADworld_XCTF/Exersice/9_string λ checksec string 
[*] '/home/l1j9m4/0_PWNable/ADworld_XCTF/Exersice/9_string/string'
    Arch:     amd64-64-little
    RELRO:    Full RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
```

Vì code bài này khá dài nên mình sẽ không để toàn bộ code decompiler ở đây mà sẽ đi sâu vào những functions có thể khai thác được mà mình thấy qua trình dịch ngược IDA64.

