# Major_Project/HE_Cloud_API/multi_client.py

import requests
from HE_Tenseal.client import send_to_cloud  # encryption function
import json

# ==== Update these URLs ====
CLOUD_1_URL = "https://he-cloud-api-charan.onrender.com/process_encrypted"  # Render cloud
CLOUD_2_URL = "https://2ace41bb-2284-4465-89c6-dc82d39a0862-00-1bpol0xejx2yp.pike.repl.co/"  

def send_to_cloud_servers(numbers):
    """
    Encrypt numbers using client.py and send to cloud URLs.
    Returns the JSON responses from clouds.
    """
    # Encrypt numbers
    ciphertext_b64 = send_to_cloud(numbers)

    # Prepare payload
    payload = {"numbers": numbers}  # Render endpoint expects original numbers (or encrypted depending on your cloud setup)

    responses = {}

    for i, url in enumerate([CLOUD_1_URL, CLOUD_2_URL], start=1):
        try:
            print(f"\nSending data to Cloud {i}: {url}")
            res = requests.post(url, json=payload, timeout=300, verify=False)
            res.raise_for_status()
            data = res.json()
            responses[f"cloud_{i}"] = data
            print(f"✅ Cloud {i} response:", data)
        except Exception as e:
            print(f"❌ Cloud {i} failed:", e)
            responses[f"cloud_{i}"] = {"error": str(e)}

    return responses

if __name__ == "__main__":
    # Example input numbers
    numbers = [1, 2, 3]  # You can also take input from console: numbers = list(map(float, input("Enter 3 numbers separated by space: ").split()))
    print("Numbers to send:", numbers)
    results = send_to_cloud_servers(numbers)
    print("\nAll cloud responses:", results)
