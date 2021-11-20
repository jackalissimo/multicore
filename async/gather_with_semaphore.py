import asyncio
import random


async def gather_with_semaphore(n: int, *tasks):
    """
    e.g.:
    await gather_with_semaphore(100, *my_coroutines)
    :param n: int
    :param tasks: usual tasks, as they were in asyncio.gather(*tasks)
    :return: list of coro responses
    """
    semaphore = asyncio.Semaphore(n)

    async def sem_task(task):
        async with semaphore:
            return await task
    return await asyncio.gather(*(sem_task(task) for task in tasks))


async def test_call(x: int):
    wait_time = random.uniform(0.01, 1.5)
    print('operation {0} will take {1:0.2f} second(s)'.format(x, wait_time))
    await asyncio.sleep(wait_time)  # I/O
    print('operation {0}'.format(x))


async def test_gather_with_semaphore():
    my_coroutines = [
        test_call(i)
        for i in range(100)
    ]
    await gather_with_semaphore(5, *my_coroutines)


if __name__ == "__main__":
    asyncio.run(test_gather_with_semaphore())
