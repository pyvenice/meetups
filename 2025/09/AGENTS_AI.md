# Agents AI

Con Ollama è possibile creare ed usare agenti con le sue API.

## Modelfile

Creando un [Modelfile](https://ollama.readthedocs.io/en/modelfile/)

```sh
cat Modelfile
FROM qwen3
SYSTEM "Sei un assistente esperto in storia romana. Rispondi sempre in italiano e in modo dettagliato."
```

Definendo un modello con il Modelfile

```sh
ollama create storico -f Modelfile
```

Che è direttamente chiamabile dalle API di Ollama

* via CLI

```sh
curl http://localhost:11434/api/chat -d '{
  "model": "storico",
  "messages": [
    {"role": "user", "content": "Raccontami la vita di Cesare."}
  ]
}'
```

* via Python

```python
from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

resp = client.chat.completions.create(
    model="storico",
    messages=[{"role": "user", "content": "Parlami della caduta di Roma."}]
)

print(resp.choices[0].message.content)
```

Con questa metodica, è possibile configurare un modello con anche

* ADAPTER, che permette di caricare un adapter sopra il modello base
* LICENSE, per aggiungere un campo informativo per distribuire il modello personalizzato
* MESSAGE, che consente di predefinire messaggi iniziali
* PARAMETER, per sovrascrivere gli hyperparameter a runtime
* TEMPLATE, per definire un prompt template usato dal modello

Ecco un esempio:

```Dockerfile
FROM qwen3
PARAMETER temperature 0.3
PARAMETER num_predict 512
TEMPLATE """{{ .System }}

Utente: {{ .Prompt }}

Assistente:"""
SYSTEM "Sei un assistente gentile che risponde solo in italiano."
MESSAGE user "Ciao!"
MESSAGE assistant "Ciao! Come posso aiutarti?"
LICENSE "MIT"
```

## WASM

Creando una pagina web che utilizzi pyodide e WASM, come proposto nella [guida](README.md).

## FastAPI

```python
from fastapi import FastAPI, Request
import requests

app = FastAPI()

OLLAMA_URL = "http://localhost:11435" # per mascherare ollama

# agente Python custom
def agente_meteo(città: str) -> str:
    return f"A {città} oggi ci sono 28°C e sole."

@app.post("/api/chat")
async def chat(request: Request):
    body = await request.json()
    messages = body.get("messages", [])
    last_message = messages[-1]["content"] if messages else ""

    # esempio di routing: se si parla di "meteo", chiama l'agente Python
    if "meteo" in last_message.lower() or "tempo" in last_message.lower():
        content = agente_meteo("Roma")
        return {
            "message": {"role": "assistant", "content": content}
        }

    # altrimenti passa la richiesta ad Ollama
    resp = requests.post(f"{OLLAMA_URL}/api/chat", json=body)
    return resp.json()
```

Che può essere tirato su con [uvicorn](https://www.uvicorn.org/)

```sh
uvicorn orchestratore:app --reload --port 11434 # per simulare ollama
```
