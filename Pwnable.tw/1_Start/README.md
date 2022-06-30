# pwnable.tw - Start

nc chall.pwnable.tw 10000

# 1) Analysis and find Bug

Đầu tiên ta kiếm tra các secure flag và xem thông tin cơ bản của file.

![checksec.png](images/checksec.png)

Chương trình 32-bit được viết hoàn toàn bằng code nAsm và không bị mất `label` các chức năng của chương trình (not stripped).

```
l1j9m4 in ~/0_PWNable_/Pwnable.tw/1_Start λ gdb -q ./start  
pwndbg: loaded 198 commands. Type pwndbg [filter] for a list.
pwndbg: created $rebase, $ida gdb functions (can be used with print/break)
Reading symbols from ./start...
(No debugging symbols found in ./start)
pwndbg> info func
All defined functions:

Non-debugging symbols:
0x08048060  _start
0x0804809d  _exit
0x080490a3  __bss_start
0x080490a3  _edata
0x080490a4  _end
pwndbg> 
```

Vì vậy ta tiến hành phân tích và tìm lỗi từ mã nguồn của chương trình bằng gdb.

```asm

```


# 2) Idea

# 3) Exploit

# 4) Source code

------------------------------------------------------
