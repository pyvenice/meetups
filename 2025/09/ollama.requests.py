import requests

url = "http://localhost:11434/api/generate"
payload = {
    "model": "qwen3",
    "prompt": "Chi ha scritto I promessi sposi?",
    "stream": False
}

res = requests.post(url, json=payload, stream=True)

for line in res.iter_lines():
    if line:
        print(line.decode("utf-8"))
