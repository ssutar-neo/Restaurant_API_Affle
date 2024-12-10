import requests
import time

API_URL = "http://localhost:8000/api/restaurants"
PARAMS = {
    "latitude": 48.023495,
    "longitude": 7.858444699999999
}

NUM_REQUESTS = 10

def benchmark_api():
    response_times = []

    for _ in range(NUM_REQUESTS):
        start_time = time.time()  
        response = requests.get(API_URL, params=PARAMS) 
        end_time = time.time()  
        response_time = (end_time - start_time) * 1000
        response_times.append(response_time)

        if response.status_code != 200:
            print(f"Error: {response.status_code}, Response: {response.json()}")

    avg_response_time = sum(response_times) / len(response_times)
    max_response_time = max(response_times)
    min_response_time = min(response_times)

    print(f"API Benchmark Results:")
    print(f"Total Requests: {NUM_REQUESTS}")
    print(f"Average Response Time: {avg_response_time:.2f} ms")
    print(f"Maximum Response Time: {max_response_time:.2f} ms")
    print(f"Minimum Response Time: {min_response_time:.2f} ms")

if __name__ == "__main__":
    benchmark_api()
