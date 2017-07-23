VERSION=0.0.1

%.o: %.c %.h
	gcc -c -fPIC -o $@ $<

libgpioctl: gpioctl.o
	gcc -shared -fPIC -Wl,-soname=$@.so -o $@.so.$(VERSION) $^ -lc

build: libgpioctl

clean:
	rm -f libgpioctl.so.$(VERSION) *.o
