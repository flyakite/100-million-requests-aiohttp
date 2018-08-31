from aiohttp import web
import os
import asyncio
import random
import logging

logging.basicConfig(
    format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%d-%m-%Y:%H:%M:%S',
    level=logging.ERROR #change to DEBUG or INFO for debuging
)
logger = logging.getLogger()

async def handle(request):
    logger.info("start_{}".format(request.match_info.get('name')))
    await asyncio.sleep(random.uniform(0, 0.1))
    logger.info("end_{}".format(request.match_info.get('name')))
    return web.Response(text="Hello, World!")

async def init():
    app = web.Application()
    app.router.add_route('GET', '/{name}', handle)
    return await loop.create_server(
        app.make_handler(), '127.0.0.1', 8888)

if __name__ == '__main__':

    loop = asyncio.get_event_loop()
    loop.run_until_complete(init())
    loop.run_forever()