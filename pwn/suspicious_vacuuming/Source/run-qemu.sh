#!/bin/bash

# todo:
#  * pull the challenge
#  * compile the challenge
#  * start the challenge
#  * set up the flag
#  * set up periodic aiden emulator

python3 -m http.server --directory /VM_config &

qemu-system-x86_64                                            \
    -nic user,hostfwd=tcp::1337-:1337,hostfwd=tcp::60022-:22 \
    -machine accel=kvm:tcg                                      \
    -m 512                                                      \
    -nographic                                                  \
    -hda plucky-server-cloudimg-amd64.img                       \
    -smbios type=1,serial=ds='nocloud;s=http://10.0.2.2:8000/' &

    # -net nic                                                    \
    # -net user                                                   \

/bin/bash