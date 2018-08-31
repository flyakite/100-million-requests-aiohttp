# Making 100 million requests with aiohttp

Inspired by Andy Balaam's [blog](https://www.artificialworlds.net/blog/2017/06/12/making-100-million-requests-with-python-aiohttp/)

This repo provides a way to make 100 million plus requests and limits the concurrent requests with a semaphore based on asyncio and aiohttp without CPU or memory exhausting.


## Runtime
Python 3.6


## Usage
Server
```bash
python server.py
```

Client
```bash
python client.py -n 100000000 -c 1000
```

