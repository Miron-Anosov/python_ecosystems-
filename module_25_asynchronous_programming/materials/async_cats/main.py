import asyncio
from pathlib import Path

import aiofiles
import aiohttp

URL = 'https://cataas.com/cat'
# CATS_WE_WANT = 10
OUT_PATH = Path(__file__).parent / 'cats'
OUT_PATH.mkdir(exist_ok=True, parents=True)
OUT_PATH = OUT_PATH.absolute()


async def get_cat(client: aiohttp.ClientSession, sem: asyncio.Semaphore, idx: int) -> bytes:
    async with sem:
        async with client.get(URL) as response:
            # print(response.status)
            result = await response.read()
            await write_to_disk(result, idx)


async def write_to_disk(content: bytes, id: int):
    file_path = "{}/{}.png".format(OUT_PATH, id)
    async with aiofiles.open(file_path, mode='wb') as f:
        await f.write(content)


async def get_all_cats(cats):
    sem = asyncio.Semaphore(10)
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(30)) as client:
        tasks = [get_cat(client, sem, i) for i in range(cats)]
        return await asyncio.gather(*tasks)


def main(cats=10):
    res = asyncio.run(get_all_cats(cats))
    # print(len(res))


if __name__ == '__main__':
    main()
