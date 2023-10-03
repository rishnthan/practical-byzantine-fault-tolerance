import aiohttp
import asyncio

async def send_request():
    for i in range(5):
        async with aiohttp.ClientSession() as session:
            data = {"data": "very-important-data"}
            async with session.post("http://localhost:8081/receive", json=data) as response:
                print(await response.text())

loop = asyncio.get_event_loop()
loop.run_until_complete(send_request())