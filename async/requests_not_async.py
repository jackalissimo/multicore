"""
Expamle of reason of threads usage.
Well, requests lib executes sequentially anyway, even if trying to make async calls.
So this example FAILS.

Should use ThreadPoolExecutor for requests lib, or not using it at all.
"""

import asyncio
import csv
import requests
from os import path
from timeit import default_timer as timer

DIR = path.realpath('.')


async def make_req(url: str):
    """
    ain't gonna work
    """
    print(url)
    res = requests.get(url)
    return res


def get_urls_list():
    file_realpath = path.join(DIR, 'csv', 'results.csv')
    urls = []
    n_urls = 0
    with open(file_realpath) as csv_urls:
        reader = csv.reader(csv_urls)
        for i, line_l in enumerate(reader):
            if i >= 300 or n_urls >= 100:
                break
            if len(line_l) < 1:
                continue
            line = line_l[0]
            parts = line.split(';')
            part0 = parts[0]
            if part0[:len('https://')] != 'https://':
                continue
            urls.append(part0)
            n_urls +=1
    return urls


async def main():
    urls = get_urls_list()
    reqs_num = len(urls)
    print("urls to fetch: {}".format(reqs_num))
    start = timer()
    tasks = [
        asyncio.create_task(make_req(url))
        for url in urls
    ]
    coros_created = timer()
    print("coros creation time {:0.3}".format(coros_created - start))

    rets = await asyncio.gather(*tasks)
    reqs_finished = timer()
    print("all requests finished {:0.3}".format(reqs_finished - start))
    print(len(rets))


if __name__ == '__main__':
    asyncio.run(main())
