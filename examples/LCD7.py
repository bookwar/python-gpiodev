from gpiodev.lcd7 import LCD7, render_digit
import time

LCD = LCD7(
    (
        26, #12
        22, #9
        17, #8
        18, #6
    ),
    (
        19, #11
        6,  #10
        4,  #7
        23, #5
        21, #1
        27, #4
        16, #2
    ),
)


while True:
    for digit in [
            (0, "j"),
            (1, "h"),
            (2, "k"),
            (3, "l"),
    ]:
        LCD.set_values(render_digit(*digit))
        time.sleep(0.005)
