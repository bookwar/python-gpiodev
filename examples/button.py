from gpiodev import GPIOHandle
import time

RedLED = GPIOHandle((19,), mode="out")
Button = GPIOHandle((18,), mode="in")

while True:

    state = Button.get_values()[0]
    print(state)
    RedLED.set_values((state,))
    time.sleep(0.1)
