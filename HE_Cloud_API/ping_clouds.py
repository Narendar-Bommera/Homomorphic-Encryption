# ping_clouds.py
import requests
import json

CLOUD_A = "https://he-cloud-api-charan.onrender.com"   # Render URL (example)
CLOUD_B = "https://2ace41bb-2284-4465-89c6-dc82d39a0862-00-1bpol0xejx2yp.pike.replit.dev"  # Replit URL (example)

def ping(url):
    try:
        r = requests.get(url, timeout=8)
        print(f"\n→ {url}")
        print("Status code:", r.status_code)
        # try to pretty-print json if returned
        try:
            obj = r.json()
            print("JSON response:")
            print(json.dumps(obj, indent=2, ensure_ascii=False))
        except Exception:
            print("Response text (non-JSON):")
            print(r.text[:1000])
    except Exception as e:
        print(f"\n→ {url}")
        print("Error:", e)

if __name__ == "__main__":
    print("Pinging Cloud A and Cloud B...")
    ping(CLOUD_A.rstrip("/"))
    ping(CLOUD_B.rstrip("/"))
    print("\nDone.")
