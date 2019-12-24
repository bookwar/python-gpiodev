from gpiodev import GPIOChip
import time

GPIO = GPIOChip()

DoubleLED = GPIO.get_handle(
    (12, 23),
    label="DoubleLED",
)

all = (1, 1)
none = (0, 0)
first = (1, 0)
second = (0, 1)

print(GPIO.line_info(12))


for state in [all, none, first, second, all, none]*10:
    DoubleLED.set_values(state)
    print(DoubleLED.get_values())
    time.sleep(1)
