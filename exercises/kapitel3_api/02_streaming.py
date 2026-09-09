"""
BLOCK 3 · Uebung 2: Streaming
=============================
Tokens erscheinen, sobald sie generiert werden – wie in ChatGPT.
Genau dieser Mechanismus laeuft nachher in eurem Vue-Frontend.
"""
from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

stream = client.chat.completions.create(
    model="qwen3.5:9b",
    extra_body={"reasoning_effort": "none"},   # sonst "denkt" Qwen 3.5 erst minutenlang
    messages=[{"role": "user", "content": "Zaehle von 1 bis 10 und kommentiere jede Zahl kurz."}],
    stream=True,
)
for chunk in stream:
    delta = chunk.choices[0].delta.content
    if delta:
        print(delta, end="", flush=True)
print()
