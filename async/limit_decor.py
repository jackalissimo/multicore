import asyncio
import random
import time
from concurrent.futures import ThreadPoolExecutor
from functools import wraps


class Limit:
    """
    Limit decorator.
    Make sure, func will not be called more than <calls> times within <period> seconds
    !FITS!: await func()
    !DOES NOT FIT!: await asyncio.gather(*tasks)
    """
    def __init__(self, calls=5, period=1.0):
        self.calls = calls
        self.period = period
        self.clock = time.monotonic
        self.last_reset = 0
        self.num_calls = 0

    def __call__(self, func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            if self.num_calls >= self.calls:
                await asyncio.sleep(self.__period_remaining())

            period_remaining = self.__period_remaining()
            if period_remaining <= 0:
                self.num_calls = 0
                self.last_reset = self.clock()

            self.num_calls += 1
            return await func(*args, **kwargs)
        return wrapper

    def __period_remaining(self):
        elapsed = self.clock() - self.last_reset
        return self.period - elapsed


@Limit(calls=5, period=2)
async def test_call(x: int):
    wait_time = random.uniform(0.01, 0.2)
    print('operation {0} will take {1:0.2f} second(s)'.format(x, wait_time))
    await asyncio.sleep(wait_time)  # I/O
    print('operation {0}'.format(x))


async def simple_worker():
    start = time.time()
    for x in range(100):
        await test_call(x + 1)
    finish = time.time()
    print("{0:.1f} sec passed".format(finish - start))


async def test_gather_task():
    tasks = [
        asyncio.ensure_future(test_call(i))
        for i in range(100)
    ]
    start = time.time()
    await asyncio.gather(*tasks)
    finish = time.time()
    print("{0:.1f} sec passed".format(finish - start))


if __name__ == '__main__':
    asyncio.run(simple_worker())
    # asyncio.run(test_gather_task())  # this fails!
