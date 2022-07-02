from pwn import *
from ctypes import *
r = CDLL("/lib/x86_64-linux-gnu/libc.so.6")
''' ldd ./token
	linux-vdso.so.1 (0x00007ffc4767b000)
	libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x00007fb3744b6000)
	/lib64/ld-linux-x86-64.so.2 (0x00007fb3746bf000)

'''
p = process('./token')	# in local v4 != guess $set $rax=........ to print flag
# p=remote('103.229.41.18',8081)	# server don't know
# gdb.attach(p)

# raw_input("DEBUG")    # test xem co debug dc server ko -> ko
# generation guess random real time 
r.srand(r.time(0))
guess = r.rand()%300
print guess

def login(user, passwd, index):
    p.sendlineafter("choice:", "2")			# choice 
    p.sendlineafter("account:", str(user))		# account = Admin
    p.sendlineafter("password:", str(passwd)) 		# passwd will compare with s2 = 0x5700060504030201 - set b *0x40100f to check
    p.sendline(str(index))				# index is guess random real time 
    a = p.recvuntil("choice:")
    print a

login("Admin\x00", p64(0x5700060504030201), guess)	# s2 global variable string addr = .rodata:000000000040144D


p.sendline("6") 

p.interactive()

'''
v4 = rbp - 34h
-> 0x401066    cmp    eax, dword ptr [rbp - 0x34]
0x040100f check pass
 
 variable check dword_60212C addr in 0x60212c
'''
