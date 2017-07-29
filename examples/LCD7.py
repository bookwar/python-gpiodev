from gpiodev.lcd7 import LCD7
import asyncio


LCD = LCD7(
    (
        26,  # 12
        22,  # 9
        17,  # 8
        18,  # 6
    ),
    (
        19,  # 11
        6,   # 10
        4,   # 7
        23,  # 5
        21,  # 1
        27,  # 4
        16,  # 2
    ),
)


async def tick(cycles):
    for counter in range(cycles):
        print('tick')
        for state in [
                " hal",
                "hall",
                "allo",
                "llo ",
                "lo h",
                "o ha",
        ]:
            LCD.state = state
            await asyncio.sleep(0.5)
    LCD.state = None


async def asynchronous():
    futures = [LCD.async_show("    "), tick(40)]
    await asyncio.wait(futures)


ioloop = asyncio.get_event_loop()
ioloop.run_until_complete(asynchronous())
ioloop.close()
