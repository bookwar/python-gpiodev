# Managing GPIO pins via character device

## Basics

For the set of GPIO lines (pins) we create an object called `GPIOHandle`, which manages their state.

State is a tuple of 0's and 1's. 

## Example

```
from gpiodev import GPIOHandle
import time

# Create handle for lines 12 and 23

DoubleLED = GPIOHandle((12,23))

# Define states of the Double LED

all = (1, 1)
none = (0, 0)
first = (1, 0)
second = (0, 1)

# Loop through the states

for state in [all, none, first, second, none, all, none]:
    DoubleLED.set_values(state)
    print(DoubleLED.get_values())
    time.sleep(1)
```

## Background

New GPIO interface has been
[introduced](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=1a46712aa99594eabe1e9aeedf115dfff0db1dfd) in the kernel.

It exposes GPIO interface a character device(`/dev/gpiochip0`) and
provides several [ioctl
syscalls](https://github.com/torvalds/linux/blob/master/include/uapi/linux/gpio.h)
for bulk operations on sets of GPIO pins.

In [gpiodev/src/gpioctl.c](gpiodev/src/gpioctl.c) we wrap the ioctl calls into
C-functions suitable for later use.

In [gpiodev/gpio.py](gpiodev/gpio.py) the ctypes bindings created and then
used to define the main GPIOHandle class.

----

Tested on [Fedora 26+ armhfp](https://arm.fedoraproject.org), Raspberry Pi 3 Model B.
