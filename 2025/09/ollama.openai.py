from openai import OpenAI
import os

client = OpenAI(
    base_url=os.environ.get("OPENAI_API_BASE"),
    api_key=os.environ.get("OPENAI_API_KEY")
)
resp = client.chat.completions.create(
    model="qwen3",
    messages=[{"role": "user", "content": "Chi ha scritto I promessi sposi?"}]
)
print(resp.choices[0].message)