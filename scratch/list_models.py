import urllib.request
import json

key = "AIzaSyDVTO_FC6kGPKzu9LMo_t7nUnNLdHG8PME"
url = f"https://generativelanguage.googleapis.com/v1beta/models?key={key}"

try:
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode())
        models = [m['name'] for m in data.get('models', [])]
        print(json.dumps(models, indent=2))
except Exception as e:
    print(f"Error: {e}")
