"""
BLOCK 3 · Uebung 3: System-Prompt & Parameter
=============================================
Aufgaben:
  1. Bring das Modell dazu, NUR auf Schweizerdeutsch zu antworten. Klappt's? Wie gut?
  2. Setz temperature=0.0 und stell dieselbe Frage 3x. Dann temperature=1.5. Unterschied?
  3. Bonus: Was passiert bei einem sehr langen Input? (Stichwort num_ctx / Kontextfenster)
"""
from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

resp = client.chat.completions.create(
    model="qwen3.5:9b",
    extra_body={"reasoning_effort": "none"},   # sonst "denkt" Qwen 3.5 erst minutenlang
    temperature=0.7,          # <- hier spielen
    messages=[
        {"role": "system", "content": "Du antwortest ausschliesslich auf Schweizerdeutsch."},  # <- und hier
        {"role": "user", "content": "Was ist ein Embedding?"},
    ],
)
print(resp.choices[0].message.content)
