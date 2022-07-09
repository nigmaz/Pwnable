.set    nomips16
    .global __start
    .text
 
__start:
    la      $t9, function
    jalr    $t9
    nop
    addiu   $v0, $zero, 4000 + 1
    move    $a0, $zero
    syscall
function:
    subu    $sp, $sp, 0x18
    sw      $ra, 0x14($sp)
 
    # write
    addiu   $v0, $zero, 4000 + 4
    la    $a0, 1
    la    $a1, hello
    la    $a2, hello_len
    syscall
 
    # read
    addiu   $v0, $zero, 4000 + 3
    move    $a0, $zero
    move    $a1, $sp
    addiu   $a2, $zero, 0x80
    syscall
 
    # write
    addiu   $v0, $zero, 4000 + 4
    la      $a0, 1
    la      $a1, hello_start
    la      $a2, hello_start_len
    syscall
 
    # write
    addiu   $v0, $zero, 4000 + 4
    la      $a0, 1
    move    $a1, $sp
    la      $a2, 20
    syscall
 
    lw      $ra, 0x14($sp)
    addiu   $sp, 0x18
    jr      $ra
    nop
 
.data
 
hello:  .asciz  "Hello World\nWhat is your name: "
    hello_len =    . - hello
hello_start:  .asciz  "Hello "
    hello_start_len =    . - hello_start

# ssh -p 2223 app-systeme-ch65@challenge03.root-me.org



 
