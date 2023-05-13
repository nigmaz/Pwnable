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
# p = remote('chall.pwnable.tw', '10203')

elf = ELF('./vuln')
libc = ELF('./libc.so.6')
context.update(binary=elf, log_level='DEBUG')
p = elf.process()
gdb.attach(p, '''
	breakrva 0x10ba
	breakrva 0x10c6
	breakrva 0x10d2
	breakrva 0x10de
''')
# v0 - check flower is existing
# v0[1] - name flower
# v0[2] - color flower // 24

def raiseFlower(length, name, color): 
	p.sendlineafter(b'choice : ', b'1')
	print(p.recvuntil(b'name :'))
	p.sendline(str(int(length)).encode())
	print(p.recvuntil(b'flower :'))
	p.sendline(name)
	print(p.recvuntil(b'flower :'))
	p.sendline(color)
	return

def listFlower():
	p.sendlineafter(b'choice : ', b'2')
	return

def removeFlower(idx):
	p.sendlineafter(b'choice : ', b'3')
	print(p.recvuntil(b'garden:'))
	p.sendline(str(int(idx)).encode())
	return

def deleteGarden():
	p.sendlineafter(b'choice : ', b'4')
	return

raiseFlower(0x100, b'A' * 0x10, b'B' * 0x10)
raiseFlower(0x100, b'C' * 0x10, b'D' * 0x10)
raiseFlower(0x100, b'E' * 0x10, b'F' * 0x10)

listFlower()
removeFlower(1)
listFlower()

deleteGarden()
raiseFlower(0x100, b'A' * 0x10, b'B' * 0x10)

p.interactive()

```
