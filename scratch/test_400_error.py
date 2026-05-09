import urllib.request
import json

key = "AIzaSyDVTO_FC6kGPKzu9LMo_t7nUnNLdHG8PME"
model = "gemini-3.1-flash-lite"
url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}"

payload = {
    "contents": [{"parts": [{"text": "안녕? 너는 누구니?"}]}]
}

data = json.dumps(payload).encode()
req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})

try:
    with urllib.request.urlopen(req) as response:
        print(response.read().decode())
except urllib.error.HTTPError as e:
    print(f"Status: {e.code}")
    print(f"Error Body: {e.read().decode()}")
except Exception as e:
    print(f"General Error: {e}")
