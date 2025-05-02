#!/usr/bin/env python3

# make bss segment executable for shellcode, otherwise
# player must use ROP as they cannot get any feedback from
# the binary to find a stack pointer

with open("./router_challenge_static", "rb+") as f:
    f.seek(0xac + 3)
    f.write(b"\x07")
