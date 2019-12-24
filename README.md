# GPIOHandle for character device

## How to

Blinking LED lights connected to pin 12 and 23:

```
from gpiodev import GPIOHandle
import time

DoubleLED = GPIOHandle((12,23,), mode="out")

all = (1,1,)
none = (0,0,)
first = (1,0,)
second = (0,1,)

for state in [all, none, first, second, none, all, none]*10:
    DoubleLED.set_values(state)
    print(DoubleLED.get_values())
    time.sleep(0.1)
```

## Background

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

Tested on [Fedora 26+ armhfp](https://arm.fedoraproject.org), Raspberry Pi 3 Model B.
