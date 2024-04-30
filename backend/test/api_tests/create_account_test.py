import aiohttp
import asyncio
import time

url = "http://127.0.0.1:8000/user/register"


async def create_account(session, url, headers, user_id):
    data = {
        "username": f"user{user_id}",
        "password": "securepassword123",
        "email": f"user{user_id}@example.com"
    }
    try:
        async with session.post(url, headers=headers, json=data) as response:
            if response.headers["Content-Type"] == "application/json":
                return response.status, await response.json()
            else:
                text = await response.text()
                return response.status, {"message": "Non-JSON response", "content": text}
    except Exception as e:
        return 500, {"message": "Request failed", "error": str(e)}


async def run_batch(session, headers, start_id, batch_size):
    tasks = []
    for i in range(start_id, start_id + batch_size):
        tasks.append(create_account(session, url, headers, i))
        await asyncio.sleep(0.01)
    return tasks


async def main():
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    async with aiohttp.ClientSession() as session:
        start_time = time.time()
        batch_size = 100
        batch_delay = 1  # Delay between batches in seconds
        responses = []

        for i in range(1, 1001, batch_size):
            tasks = await run_batch(session, headers, i, batch_size)
            batch = await asyncio.gather(*tasks)
            responses.extend(batch)
            await asyncio.sleep(batch_delay)  # Delay between batches

        end_time = time.time()

        success_count = sum(1 for response in responses if response[0] == 200)
        fail_count = 1000 - success_count
        duration = end_time - start_time
        print(f"Successes: {success_count}")
        print(f"Failures: {fail_count}")
        print(f"Time taken ({1000} requests): {duration:.2f} seconds.")


asyncio.run(main())
