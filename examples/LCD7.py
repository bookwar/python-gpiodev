from gpiodev.lcd7 import LCD7
import asyncio


LCD = LCD7(
    digits=(26, 22, 17, 18),
    segments=(19, 6, 4, 23, 21, 27, 16),
)


async def async_write(strings, delay=0.1):
    for string in strings:
        print(string)
        LCD.state = string
        if not string:
            LCD.state = string
            return
        await asyncio.sleep(delay + 0.5 * len(string))


async def asynchronous():
    futures = [
        LCD.async_show_string(" "),
        async_write([
            "hello ",
            "1234 ",
            " 15 ",
            "6789",
            None,
        ]
        )]
    await asyncio.wait(futures)


ioloop = asyncio.get_event_loop()
ioloop.run_until_complete(asynchronous())
ioloop.close()
