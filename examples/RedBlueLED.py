from gpiodev import GPIOHandle
import time

RedBlueLED = GPIOHandle((26, 21), mode="out")

print(RedBlueLED.get_values())

RedBlueLED.set_values((1, 0))
print(RedBlueLED.get_values())
time.sleep(5)
RedBlueLED.set_values((1, 1))
print(RedBlueLED.get_values())
time.sleep(5)
RedBlueLED.set_values((0, 1))
print(RedBlueLED.get_values())
time.sleep(5)
