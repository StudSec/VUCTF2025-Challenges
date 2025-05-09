CFLAGS += -fstack-protector-strong -mshstk -fcf-protection=full -Wl,-z,relro -Wall -g

all: roomba_ids

roomba_ids: roomba_ids.c
	gcc $(CFLAGS) ./roomba_ids.c -lc -static -o ./roomba_ids
