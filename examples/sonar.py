from gpiodev import GPIOHandle, GPIOEventHandle
import time

class Sonar():

    def __init__(self, echo_pin, trigger_pin):
        self.echo_pin = echo_pin
        self.trigger_pin = trigger_pin

        self.trigger_handle = GPIOHandle((self.trigger_pin,), mode="out")
        self.echo_handle = GPIOEventHandle(self.echo_pin, mode="both")

    def trigger(self):
        self.trigger_handle.flip()
        self.trigger_handle.flip()

    def measure(self):
        self.trigger()
        start = self.echo_handle.get()[0]
        print("Start", start)
        stop = self.echo_handle.get()[0]
        print("Stop", stop)

        return (stop - start)*340.0/2.0

S = Sonar(echo_pin=20, trigger_pin=21)

while True:
    print(S.measure())
    time.sleep(5)



