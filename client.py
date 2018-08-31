from aiohttp import ClientSession
import argparse
import asyncio
import sys
import resource

def get_mem():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1000000

async def run(session, number_of_requests, concurrent_limit):
    base_url = "http://localhost:8888/{}"
    tasks = []
    responses = []
    sem = asyncio.Semaphore(concurrent_limit)

    async def fetch(i):
        url = base_url.format(i)
        async with session.get(url) as response:
            response = await response.read()
            sem.release()
            responses.append(response)
            if i % 100 == 0:
                for task in tasks:
                    if task.done():
                        tasks.remove(task)
                print("n:{:10d} tasks:{:10d} {:.1f}MB".format(i, len(tasks), get_mem()))
            return response

    for i in range(1, number_of_requests+1):
        await sem.acquire()
        url = base_url.format(i)
        task = asyncio.ensure_future(fetch(i))
        tasks.append(task)

    await asyncio.wait(tasks)
    print("total_responses: {}".format(len(responses)))
    return responses

async def main(number_of_requests, concurrent_limit):
    async with ClientSession() as session:
        responses = await asyncio.ensure_future(run(session, number_of_requests, concurrent_limit))
        return

if __name__ == '__main__':
    """
    run: python client.py -n 1000 -c 100
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-n')
    parser.add_argument('-c')
    args = parser.parse_args()
    number_of_requests = int(args.n) if args.n else 10000
    concurrent_limit = int(args.c) if args.c else 1000
    print("number_of_requests: {}, concurrent_limit: {}".format(number_of_requests, concurrent_limit))
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(number_of_requests, concurrent_limit))
    loop.close()
    