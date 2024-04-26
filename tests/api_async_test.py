import aiohttp
import asyncio
import time

url = "http://127.0.0.1:8000/game/equip-item/4"
token = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZXhwIjoxODk0MTQ0MjQ1fQ.dCMvTHoNeTg2ZVPIM2Kd-hk8I3fSWKDCYFh1SrYglQs"
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

        success_count = sum(1 for response in responses if response['message'] in ['equipped', 'unequipped'])
        fail_count = amount_requests - success_count

        duration = end_time - start_time
        print(f"Successes: {success_count}")
        print(f"Failures: {fail_count}")
        print(f"Time taken ({amount_requests} requests): {duration:.2f} seconds.")

asyncio.run(main())