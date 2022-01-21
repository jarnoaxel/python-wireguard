CC=gcc
CFLAGS = -Wall -g -O -fPIC $(shell pkg-config --cflags python3)
RM= rm -f
.PHONY: all clean

all: library.so
clean:
	$(RM) *.o *.so

library.so: python_interface.o wireguard.o
	$(LINK.c) -shared $^ -o $@

python_interface.o: python_interface.c

wireguard.o: wireguard.c wireguard.h
