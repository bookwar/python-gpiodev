# GPIOHandle for character device

New GPIO interface has been
[introduced](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=1a46712aa99594eabe1e9aeedf115dfff0db1dfd)
recently.

It exposes GPIO interface as `/dev/gpiochip0` character device and
provides several [ioctl
syscalls](https://github.com/torvalds/linux/blob/master/include/uapi/linux/gpio.h)
for bulk operations on sets of GPIO pins.

In [gpiodev/src/gpioctl.c](gpiodev/src/gpioctl.c) we wrap the ioctl calls into
C-functions suitable for later use.

In [gpiodev/gpio.py](gpiodev/gpio.py) the ctypes bindings created and then
used to define the main GPIOHandle class.

Check [examples](examples) for usage.

----

Tested on Fedora 26 armv7, Raspberry Pi 3 Model B.
