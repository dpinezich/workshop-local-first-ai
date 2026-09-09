"""
BLOCK 3 · Uebung 1: Dein erster lokaler API-Call
================================================
DER Aha-Moment: Das ist der ganz normale OpenAI-Client.
Einzige Aenderung: base_url zeigt auf deinen Laptop.

Start:  python 01_erster_call.py
"""
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:11434/v1",   # <- DIE eine Zeile.
    api_key="ollama",                        # Pflichtfeld, Wert egal
)

resp = client.chat.completions.create(
    model="qwen3.5:9b",
    extra_body={"reasoning_effort": "none"},   # sonst "denkt" Qwen 3.5 erst minutenlang
    messages=[
        {"role": "user", "content": "Erklaere in zwei Saetzen, warum du ohne Internet funktionierst."},
    ],
)
print(resp.choices[0].message.content)
