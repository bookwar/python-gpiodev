import os, ctypes, ctypes.util

c32 = ctypes.c_char * 32
GPIOHANDLES_MAX = 64
cul_MAX = ctypes.c_ulong * GPIOHANDLES_MAX
cu8_MAX = ctypes.c_ubyte * GPIOHANDLES_MAX

class _gpiochip_info (ctypes.Structure):
    _fields_ = [
        ("name", c32),
        ("label", c32),
        ("lines", ctypes.c_long),
    ]

class _gpioline_info (ctypes.Structure):
    _fields_ = [
        ("line", ctypes.c_long),
        ("flags", ctypes.c_ulong),
        ("name", c32),
        ("consumer", c32),
    ]

class _gpiohandle_request (ctypes.Structure):
    _fields_ = [
        ('lineoffsets', cul_MAX),
        ('flags', ctypes.c_ulong),
        ('default_values', cu8_MAX),
        ('consumer_label', c32),
        ('lines', ctypes.c_ulong),
        ('fd', ctypes.c_int),
    ]

class _gpioevent_request (ctypes.Structure):
    _fields_ = [
        ('lineoffset', ctypes.c_ulong),
        ('handleflags', ctypes.c_ulong),
        ('eventflags', ctypes.c_ulong),
        ('consumer_label', c32),
        ('fd', ctypes.c_int),
    ]

def _gpiohandle_data():
    return ctypes.create_string_buffer(GPIOHANDLES_MAX)

########################################################

libgpioctl = ctypes.CDLL('./libgpioctl.so.0.0.1')
fd = os.open("/dev/gpiochip0", os.O_RDWR)

info = gpiochip_info()

status = libgpioctl.get_chipinfo(fd, ctypes.byref(info))

print status
print info.lines
