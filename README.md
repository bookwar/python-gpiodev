# Managing GPIO pins via character device

## Basics

For the set of GPIO lines (pins) we create an object called `GPIOHandle`, which manages their state. State is a tuple of 0's and 1's, one number per line.

This library doesn't require root access to the system, but it needs a read-write access to the gpiochip device. By default it uses `/dev/gpiochip0`.

To allow read-write access to the device for the user, run:

    $ sudo chmod a+rw /dev/gpiochip0

Note that the system might have several GPIO chips, some of them can be exposed to the user (as /dev/gpiochip0 on Raspberry Pi) and some of them might be responsible for system functions, like WakeOnLan or system LED lights. Be carefull when choosing the device and allowing user access to it.

You can check the info on the GPIOChip device, by accessing its info() method. See example below.

## Example

```
from gpiodev import GPIOHandle
import time

# Request handle for lines 12 and 23 from default /dev/gpiochip0 

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

## Use another device

To use another gpiochip device, for example `/dev/gpiochip1`, you can use a different way to setup a handle:

```
from gpiodev import GPIOChip

GPIO = GPIOChip("/dev/gpiochip1")

# Check info on the gpio chip

print(GPIO.info())

# Request handle for lines 12 and 23 from /dev/gpiochip1

DoubleLED = GPIO.get_handle((12,23)) # This will fail on RaspberryPi as /dev/gpiochip1 is a system gpio chip, with only 8 lines.

```

## Background

New GPIO interface has been
[introduced](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=1a46712aa99594eabe1e9aeedf115dfff0db1dfd) in the kernel.

It exposes GPIO interface a character device(`/dev/gpiochip0`) and
provides several [ioctl
syscalls](https://github.com/torvalds/linux/blob/master/include/uapi/linux/gpio.h)
for bulk operations on sets of GPIO pins.

Unlike Python bindings to the [libgpiod](https://git.kernel.org/pub/scm/libs/libgpiod/libgpiod.git/) C-library, we work with the kernel interface (ioctl calls) directly.

In [gpiodev/src/gpioctl.c](gpiodev/src/gpioctl.c) we wrap the ioctl calls into
C-functions suitable for later use.

In [gpiodev/gpio.py](gpiodev/gpio.py) the ctypes bindings are created and then
used to define the main GPIOHandle class.

----

Tested on [Fedora 26+ armhfp](https://arm.fedoraproject.org), Raspberry Pi 3 Model B.
