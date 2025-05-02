# the challenge
The studsec anti-roomba response team has intercepted a shipment of routers!
We found they may be useful as they are equipped with an additional configuration
interface port, which may be vulnerable. But nmap did not work? 

Dump the flash and find out what is going on! Look for any vulnerabilities in 
the system and figure out how to exploit them. 

The system runs MIPS, remember that
you can run statically linked mips binaries using the qemu userspace emulators:
`qemu-mips ./binary -g 64532` in combination with `gdb-multiarch -ex target remote :64532`.
If gdb-multiarch is not available, you can try to use it raw, or in an ubuntu 
docker container provided in the handout.

Good luck!
