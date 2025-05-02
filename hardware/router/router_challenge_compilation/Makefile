# build helloworld executable when user executes "make"
CC = /tools/bin/mips-buildroot-linux-uclibc-gcc
LD_LIBRARY_PATH=$(pwd)
CFLAGS = -fno-stack-protector -z execstack -no-pie

# assembler: /usr/mips-linux-gnu/bin/as
all: challenge-static

challenge-static:
	$(CC) $(CFLAGS) -static ./libc.a router_challenge.c -o ./router_challenge_static
	chmod 777 ./router_challenge_static
	./patch_elf.py


default: all

# remove object files and executable when user executes "make clean"
clean:
	rm -f ./router_challenge_static
