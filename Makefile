CC=gcc
CFLAGS = -Wall -g -O -fPIC $(shell pkg-config --cflags python3)
RM= rm -f
.PHONY: all clean

all: python_wireguard/bin/py-wireguard.so
clean:
	$(RM) src/*.o python_wireguard/bin/*.so

python_wireguard/bin/py-wireguard.so: src/python_interface.o src/wireguard.o
	$(LINK.c) -shared $^ -o $@

src/python_interface.o: src/python_interface.c

src/wireguard.o: src/wireguard.c src/wireguard.h
