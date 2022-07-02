   0x0000000000400727 <+0>:	push   rbp
   0x0000000000400728 <+1>:	mov    rbp,rsp
   0x000000000040072b <+4>:	sub    rsp,0x30
   0x000000000040072f <+8>:	mov    BYTE PTR [rbp-0x20],0x55
   0x0000000000400733 <+12>:	mov    BYTE PTR [rbp-0x1f],0x48
   0x0000000000400737 <+16>:	mov    BYTE PTR [rbp-0x1e],0x31
   0x000000000040073b <+20>:	mov    BYTE PTR [rbp-0x1d],0xd2
   0x000000000040073f <+24>:	mov    BYTE PTR [rbp-0x1c],0x48
   0x0000000000400743 <+28>:	mov    BYTE PTR [rbp-0x1b],0x31
   0x0000000000400747 <+32>:	mov    BYTE PTR [rbp-0x1a],0xf6
   0x000000000040074b <+36>:	mov    BYTE PTR [rbp-0x19],0x48
   0x000000000040074f <+40>:	mov    BYTE PTR [rbp-0x18],0xbb
   0x0000000000400753 <+44>:	mov    BYTE PTR [rbp-0x17],0x2f
   0x0000000000400757 <+48>:	mov    BYTE PTR [rbp-0x16],0x62
   0x000000000040075b <+52>:	mov    BYTE PTR [rbp-0x15],0x69
   0x000000000040075f <+56>:	mov    BYTE PTR [rbp-0x14],0x9e
   0x0000000000400763 <+60>:	mov    BYTE PTR [rbp-0x13],0x2f
   0x0000000000400767 <+64>:	mov    BYTE PTR [rbp-0x12],0x2f
   0x000000000040076b <+68>:	mov    BYTE PTR [rbp-0x11],0x73
   0x000000000040076f <+72>:	mov    BYTE PTR [rbp-0x10],0x68
   0x0000000000400773 <+76>:	mov    BYTE PTR [rbp-0xf],0x53
   0x0000000000400777 <+80>:	mov    BYTE PTR [rbp-0xe],0x54
   0x000000000040077b <+84>:	mov    BYTE PTR [rbp-0xd],0x5f
   0x000000000040077f <+88>:	mov    BYTE PTR [rbp-0xc],0x5b
   0x0000000000400783 <+92>:	mov    BYTE PTR [rbp-0xb],0x3b
   0x0000000000400787 <+96>:	mov    BYTE PTR [rbp-0xa],0x11
   0x000000000040078b <+100>:	mov    BYTE PTR [rbp-0x9],0x5
   0x000000000040078f <+104>:	lea    rdi,[rip+0x197]        # 0x40092d
   0x0000000000400796 <+111>:	call   0x400580 <puts@plt>
   0x000000000040079b <+116>:	lea    rax,[rbp-0x2a]
   0x000000000040079f <+120>:	mov    rsi,rax
   0x00000000004007a2 <+123>:	lea    rdi,[rip+0x19e]        # 0x400947
   0x00000000004007a9 <+130>:	mov    eax,0x0
   0x00000000004007ae <+135>:	call   0x4005b0 <__isoc99_scanf@plt>
   0x00000000004007b3 <+140>:	lea    rax,[rbp-0x2a]
   0x00000000004007b7 <+144>:	mov    rsi,rax
   0x00000000004007ba <+147>:	lea    rdi,[rip+0x18b]        # 0x40094c
   0x00000000004007c1 <+154>:	mov    eax,0x0
   0x00000000004007c6 <+159>:	call   0x400590 <printf@plt>
   0x00000000004007cb <+164>:	mov    DWORD PTR [rbp-0x4],0x0
   0x00000000004007d2 <+171>:	jmp    0x400836 <useme+271>
   0x00000000004007d4 <+173>:	mov    eax,DWORD PTR [rbp-0x4]
   0x00000000004007d7 <+176>:	mov    esi,eax
   0x00000000004007d9 <+178>:	lea    rdi,[rip+0x181]        # 0x400961
   0x00000000004007e0 <+185>:	mov    eax,0x0
   0x00000000004007e5 <+190>:	call   0x400590 <printf@plt>
   0x00000000004007ea <+195>:	lea    rax,[rbp-0x30]
   0x00000000004007ee <+199>:	mov    rsi,rax
   0x00000000004007f1 <+202>:	lea    rdi,[rip+0x171]        # 0x400969
   0x00000000004007f8 <+209>:	mov    eax,0x0
   0x00000000004007fd <+214>:	call   0x4005b0 <__isoc99_scanf@plt>
   0x0000000000400802 <+219>:	mov    eax,DWORD PTR [rbp-0x30]
   0x0000000000400805 <+222>:	cmp    eax,0x1
   0x0000000000400808 <+225>:	jne    0x400818 <useme+241>
   0x000000000040080a <+227>:	lea    rdi,[rip+0x15b]        # 0x40096c
   0x0000000000400811 <+234>:	call   0x400580 <puts@plt>
   0x0000000000400816 <+239>:	jmp    0x400832 <useme+267>
   0x0000000000400818 <+241>:	mov    eax,DWORD PTR [rbp-0x30]
   0x000000000040081b <+244>:	mov    edx,eax
   0x000000000040081d <+246>:	mov    eax,DWORD PTR [rbp-0x4]
   0x0000000000400820 <+249>:	cdqe   
   0x0000000000400822 <+251>:	mov    BYTE PTR [rbp+rax*1-0x20],dl
   0x0000000000400826 <+255>:	lea    rdi,[rip+0x148]        # 0x400975
   0x000000000040082d <+262>:	call   0x400580 <puts@plt>
   0x0000000000400832 <+267>:	add    DWORD PTR [rbp-0x4],0x1
   0x0000000000400836 <+271>:	cmp    DWORD PTR [rbp-0x4],0x17
   0x000000000040083a <+275>:	jle    0x4007d4 <useme+173>
   0x000000000040083c <+277>:	lea    rdx,[rbp-0x20]
   0x0000000000400840 <+281>:	mov    eax,0x0
   0x0000000000400845 <+286>:	call   rdx
   0x0000000000400847 <+288>:	nop
   0x0000000000400848 <+289>:	leave  
   0x0000000000400849 <+290>:	ret  
