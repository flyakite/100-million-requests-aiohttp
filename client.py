from aiohttp import ClientSession
import argparse
import asyncio
import sys

async def run(session, number_of_requests, concurrent_limit):
    base_url = "http://localhost:8888/{}"
    tasks = []
    responses = []
    sem = asyncio.Semaphore(concurrent_limit)

    async def fetch(url):
        async with session.get(url) as response:
            response = await response.read()
            sem.release()
            responses.append(response)
            return response

    for i in range(number_of_requests):
        await sem.acquire()
        url = base_url.format(i)
        task = asyncio.ensure_future(fetch(url))
        tasks.append(task)
        for task in tasks:
            if task.done():
                tasks.remove(task)
    await asyncio.wait(tasks)
    return responses


async def main(number_of_requests, concurrent_limit):
    async with ClientSession() as session:
        responses = await asyncio.ensure_future(run(session, number_of_requests, concurrent_limit))
        print(responses)
        return

if __name__ == '__main__':
    """
    run: python client.py -n 1000 -c 100
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-n')
    parser.add_argument('-c')
    args = parser.parse_args()
    number_of_requests = int(args.n) if args.n else 1000
    concurrent_limit = int(args.c) if args.c else 100
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(number_of_requests, concurrent_limit))
    loop.close()
    
    