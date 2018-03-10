from gpiodev import GPIOEventHandle

Button = GPIOEventHandle(17, mode="rising")

while True:
    print("reading")
    print(Button.get())
