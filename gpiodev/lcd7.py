from gpiodev import GPIOHandle
import asyncio

# LCD pins

#       12 11 10 9 8 7
#  __    __      __    __
# |  |  |  |    |  |  |  |
# |__|  |__|  . |__|  |__|
# |  |  |  |  . |  |  |  |
# |__|. |__|.   |__|. |__|.
#
#       1 2 3 4 5 6
#
#  Mapped to
#   1     2        3     4
#
#  -5-    __       __    __
# 6   |  |  |     |  |  |  |
# |   7  |__|  .  |__|  |__|
#  -8-         12
# 9   |  |  |  .  |  |  |  |
# |  10  |__|.    |__|. |__|.
#  -11-

DIGIT = [
    (0, 1, 1, 1),
    (1, 0, 1, 1),
    (1, 1, 0, 1),
    (1, 1, 1, 0),
]

SYMBOL = {
    " ": (0, 0, 0, 0, 0, 0, 0),
    "1": (0, 0, 1, 0, 0, 1, 0),
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
    "r": (0, 0, 0, 0, 1, 1, 0),
    "s": (1, 1, 0, 1, 0, 1, 1),
}


def render_digit(digit, symbol):
    return DIGIT[digit] + SYMBOL[symbol]


class LCD7(GPIOHandle):

    def __init__(self, digits, segments):
        self.digits = digits
        self.segments = segments
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

    async def async_show(self, state=None):
        if state:
            self.state = state

        while self.state:
            for index, symbol in enumerate(self.state):
                self.set_values(render_digit(index, symbol))
                await asyncio.sleep(0.001)
