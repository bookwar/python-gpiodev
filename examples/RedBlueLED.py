from gpiodev import GPIOHandle
import time

RedBlueLED = GPIOHandle((26, 21), mode="out")

print(RedBlueLED.get_values())

states = [
    (1, 0),
    (0, 1),
    (1, 1),
]

for state in states:
    RedBlueLED.set_values(state)
    print(RedBlueLED.get_values())
    time.sleep(5)
