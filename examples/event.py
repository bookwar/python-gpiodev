from gpiodev import GPIOEventHandle
import time

Button = GPIOEventHandle(17, mode="rising")

while True:
    print("reading")
    print(Button.get())
