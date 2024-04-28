import aiohttp
import asyncio
import time

url = "http://127.0.0.1:8000/game/equip-item/4"
code = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZXhwIjoxNzI1MDM5MjcxfQ.artounSV1aeeyBFmDE-5PmypUOSQLgyyq-sgrwSE2dc"
token = f"Bearer {code}"

headers = {
    "Accept": "application/json",
    "Authorization": token
}

amount_requests = 1000

async def fetch(session, url, headers):
    async with session.post(url, headers=headers) as response:
        return response.status

async def main():
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, url, headers) for _ in range(amount_requests)]
        start_time = time.time()
        responses = await asyncio.gather(*tasks)
        end_time = time.time()

        success_count = sum(1 for response in responses if response == 200)
        fail_count = amount_requests - success_count

        duration = end_time - start_time
        print(f"Successes: {success_count}")
        print(f"Failures: {fail_count}")
        print(f"Time taken ({amount_requests} requests): {duration:.2f} seconds.")

asyncio.run(main())


"""
Old sign in:
    14 fetched - 1050 returned

Old Equipping/Un:
    Transactions per second: 
    ~320 transactions, ~320 commits, ~310 rollbacks
    
    Tuples in: 
    ~600 updates
    
    Tuples out: 
    ~56000 fetched, ~62000 returned
    
    Block I/O: 
    ~89000 hits
"""