   0x8048060 <_start>:		push   esp
   0x8048061 <_start+1>:	push   0x804809d
   0x8048066 <_start+6>:	xor    eax,eax
   0x8048068 <_start+8>:	xor    ebx,ebx
   0x804806a <_start+10>:	xor    ecx,ecx
   0x804806c <_start+12>:	xor    edx,edx

   0x804806e <_start+14>:	push   0x3a465443
   0x8048073 <_start+19>:	push   0x20656874
   0x8048078 <_start+24>:	push   0x20747261
   0x804807d <_start+29>:	push   0x74732073
   0x8048082 <_start+34>:	push   0x2774654c

   0x8048087 <_start+39>:	mov    ecx,esp
   0x8048089 <_start+41>:	mov    dl,0x14
   0x804808b <_start+43>:	mov    bl,0x1
   0x804808d <_start+45>:	mov    al,0x4
   0x804808f <_start+47>:	int    0x80

   0x8048091 <_start+49>:	xor    ebx,ebx
   0x8048093 <_start+51>:	mov    dl,0x3c
   0x8048095 <_start+53>:	mov    al,0x3
   0x8048097 <_start+55>:	int    0x80

   0x8048099 <_start+57>:	add    esp,0x14
   0x804809c <_start+60>:	ret    

   0x804809d <_exit>:		pop    esp
   0x804809e <_exit+1>:		xor    eax,eax
   0x80480a0 <_exit+3>:		inc    eax
   0x80480a1 <_exit+4>:		int    0x80
   
   
