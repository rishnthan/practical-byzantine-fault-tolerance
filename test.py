import asyncio
import aiohttp

data = {
    "data": "very-important-data",}

async def main():
    for i in range(5):
        async with aiohttp.ClientSession() as session:
            async with session.post('http://localhost:8080/receive', json=data) as resp:
                print(await resp.text)

asyncio.run(main())