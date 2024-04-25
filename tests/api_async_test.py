import requests
import time

url = "http://127.0.0.1:8002/game/equip-item/60"
token = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyIiwiZXhwIjoxODkzOTg5NzAxfQ.FcLiOEeirdLaQEtO-kyzcQyWzJnogYPxuDFVSAZ64ts"
headers = {
    "Accept": "application/json",
    "Authorization": token
}

amount_requests = 1000
start_time = time.time()
success_count = 0
fail_count = 0

for i in range(amount_requests):
    response = requests.post(url, headers=headers)
    if response.status_code == 200:
        success_count += 1
    else:
        fail_count += 1
    if i % 100 == 0:
        print(f"Request {i + 1}: Status {response.status_code}")

end_time = time.time()
duration = end_time - start_time
print(f"Successes: {success_count}")
print(f"Failures: {fail_count}")
print(f"Time taken ({amount_requests} requests): {duration:.2f} seconds.")