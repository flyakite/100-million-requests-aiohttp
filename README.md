# Making 100 million requests with aiohttp

Inspired by Andy Balaam's [blog](https://www.artificialworlds.net/blog/2017/06/12/making-100-million-requests-with-python-aiohttp/)

Creating huge amount of asynchronous tasks all at once would encounter memory error.
This repo provides a way to make 100 million plus requests using asyncio and aiohttp. We limits the concurrent requests with a simple semaphore to prevent CPU or memory exhausting.




## Runtime
Python 3.6


## Usage
Server
```bash
python server.py
```

Client, e.g., make 100,000,000 total requests, 1,000 concurrent requests
```bash
python client.py -n 100000000 -c 1000
```

