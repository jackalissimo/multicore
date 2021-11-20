"""
Do not DOS anything with async tasks.
"""

import asyncio
from random import randint
from time import time


async def blocking_op(code):
    wait_time = randint(1, 3)
    print('operation {0} will take {1} second(s)'.format(code, wait_time))
    await asyncio.sleep(wait_time)  # I/O, context will switch to main function
    print('operation {0}'.format(code))
    

sem = asyncio.Semaphore(4)      # will be having max 4 blocking tasks running at once
sem2 = asyncio.Semaphore(10)


async def do_not_dos(i):
    async with sem:  # semaphore limits num of simultaneous tasks
        return await blocking_op(i)


async def main():
    tasks = [
        asyncio.ensure_future(do_not_dos(i))  # creating task starts coroutine
        for i
        in range(15)
    ]
    start = time()
    await asyncio.gather(*tasks)  # await moment all blocking operations done
    finish = time()
    print("{0:.1f} sec passed".format(finish - start))


if __name__ ==  '__main__':
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()

