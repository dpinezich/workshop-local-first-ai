"""BLOCK 4: Bild beschreiben mit lokalem Vision-Modell.
Aufruf: python vision_beschreiben.py <bild.jpg>"""
import base64, sys
from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
pfad = sys.argv[1] if len(sys.argv) > 1 else "rechnung.png"
b64 = base64.b64encode(open(pfad, "rb").read()).decode()

resp = client.chat.completions.create(
    model="qwen3.5:9b",
    extra_body={"reasoning_effort": "none"},   # sonst "denkt" Qwen 3.5 erst minutenlang
    messages=[{"role": "user", "content": [
        {"type": "text", "text": "Beschreibe dieses Bild praezise auf Deutsch."},
        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}},
    ]}],
)
print(resp.choices[0].message.content)
