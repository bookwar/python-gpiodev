from gpiodev import GPIOHandle
import asyncio

'''

LCD7 is a device with four 7-segment LED digits to show. 7 segments
are not enough to show arbitraty letters, but it can be used as clocks
or counter.

Though there are 4x7 = 28 LED segments to switch on and off, it uses
only 12 GPIO pins. 4 pins are used to choose the active digit, 7 pins
- to switch on segments for a digit, and one additional pin controls
central dots (not implemented here).

Abstract pins used in LCD7 class implementation are:

Digits:

```
  0     1      2     3
```

Segments:

```
  --0--
 |     |
 1     2
 |     |
  --3--
 |     |
 4     5
 |     |
  --6--
```

If we enumerate physical pins on a device in a following manner:

```
    12 11 10  9  8  7
     |  |  |  |  |  |
 __    __      __    __
|  |  |  |    |  |  |  |
|__|  |__|  . |__|  |__|
|  |  |  |  . |  |  |  |
|__|. |__|.   |__|. |__|.

     |  |  |  |  |  |
     1  2  3  4  5  6
```

Then to setup the LCD7 class one needs to specify the input pins
in the following order:

```
Digits       Segments     Dots

0)  12       0)  11       0) 3 (not used)
1)  9        1)  10
2)  8        2)  7
3)  6        3)  5
             4)  1
             5)  4
             6)  2
```

The mapping might be different for your device though.

'''


DIGIT = [
    (0, 1, 1, 1),
    (1, 0, 1, 1),
    (1, 1, 0, 1),
    (1, 1, 1, 0),
]

SYMBOL = {
    " ": (0, 0, 0, 0, 0, 0, 0),
    "0": (1, 1, 1, 0, 1, 1, 1),
    "1": (0, 0, 1, 0, 0, 1, 0),
    "2": (1, 0, 1, 1, 1, 0, 1),
    "3": (1, 0, 1, 1, 0, 1, 1),
    "4": (0, 1, 1, 1, 0, 1, 0),
    "5": (1, 1, 0, 1, 0, 1, 1),
    "6": (1, 1, 0, 1, 1, 1, 1),
    "7": (1, 0, 1, 0, 0, 1, 0),
    "8": (1, 1, 1, 1, 1, 1, 1),
    "9": (1, 1, 1, 1, 0, 1, 1),
    "a": (1, 1, 1, 1, 1, 1, 0),
    "b": (0, 1, 0, 1, 1, 1, 1),
    "c": (1, 1, 0, 0, 1, 0, 1),
    "d": (0, 0, 1, 1, 1, 1, 1),
    "e": (1, 1, 0, 1, 1, 0, 1),
    "f": (1, 1, 0, 1, 1, 0, 0),
    "g": (1, 1, 0, 0, 1, 1, 1),
    "h": (0, 1, 1, 1, 1, 1, 0),
    "i": (0, 0, 1, 0, 0, 1, 0),
    "j": (0, 0, 1, 0, 0, 1, 1),
    "k": (0, 1, 1, 1, 1, 1, 0),
    "l": (0, 1, 0, 0, 1, 0, 1),
    "m": (1, 0, 0, 0, 0, 1, 1),
    "n": (0, 0, 0, 0, 1, 1, 1),
    "o": (1, 1, 1, 0, 1, 1, 1),
    "p": (1, 1, 1, 1, 1, 0, 0),
    "q": (1, 1, 1, 1, 0, 0, 1),
    "r": (0, 0, 0, 1, 1, 0, 0),
    "s": (1, 1, 0, 1, 0, 1, 1),
}


def _render_gpio_state(digit, symbol):
    '''Return tuple with values for GPIOHandle pins.

    digit is a number from 0 to 3
    symbol is one character

    If symbol is not present in SYMBOL dictionary - show nothing.

    '''
    return DIGIT[digit] + SYMBOL.get(symbol, SYMBOL[" "])


class LCD7(GPIOHandle):

    def __init__(self, digits, segments):
        self.digits = digits
        self.segments = segments
        self.window_size = len(digits)

        lines = self.digits + self.segments
        defaults = (
            (1,)*len(self.digits)
            + (0,)*len(self.segments)
        )
        GPIOHandle.__init__(
            self,
            lines,
            defaults=defaults,
            mode="out",
        )
        self.state = None

    async def async_show_state(self, state=None, led_delay=0.005):
        '''Show current state on the display.

        We loop through characters and render them on a corresponding
        digits.

        State should be a four character iterable (for example, string).
        If state is given, reset the LCD display to it. If state is
        not provided, check for the self.state class variable.

        Looping is done asynchronously in a background. Loop will stop
        as soon as the self.state class variable is set to None.

        '''
        if state:
            self.state = state

        while self.state:
            for index, symbol in enumerate(self.state):
                self.set_values(_render_gpio_state(index, symbol))
                await asyncio.sleep(led_delay)

    async def async_show_string(self, string=None, delay=0.5, led_delay=0.005):
        '''Show the string on display.

        Create a sliding window on the string and loop through the string
        characters rendering the window on a display.

        delay (in seconds) specifies the delay between window shifts.

        led_delay (in seconds) is the maximum delay we can allow for a
        segment to be off, without it being dimmed.

        If string is given, reset the LCD display state to it. If it
        is not provided, check for the self.state class variable.

        Looping is done asynchronously in a background. Loop will stop
        as soon as the self.state class variable is set to None.

        Note that the change of the state will be noticed only at the end
        of the sliding cycle: we show the full string first before switching
        to a new one .

        '''

        string_ticks = int(delay / led_delay / self.window_size)

        if string:
            self.state = string

        while self.state:
            string = self.state
            size = len(string)
            for cursor in range(size):
                print("!!%s" % string)
                for counter in range(string_ticks):
                    for index in range(self.window_size):
                        symbol = string[(cursor + index) % size]
                        self.set_values(_render_gpio_state(index, symbol))

                        await asyncio.sleep(led_delay)

        self.set_values(self.defaults)
