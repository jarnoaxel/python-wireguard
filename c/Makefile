CC=gcc
CFLAGS = -Wall -g -O -fPIC $(shell pkg-config --cflags python3)
RM= rm -f
.PHONY: all clean

all: library.so
clean:
	$(RM) *.o *.so

library.so: hello_world.o wireguard.o
	$(LINK.c) -shared $^ -o $@

hello_world.o: hello_world.c

wireguard.o: wireguard.c wireguard.h