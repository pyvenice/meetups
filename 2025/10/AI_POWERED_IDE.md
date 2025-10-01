# Coding assistants

Uno sviluppatore principalmente vive sul proprio IDE. E quel particolare IDE è sacro, non si tocca.

Non siamo qui per parlare del proprio IDE, ma di come potenziarlo con **#LanguageModel** **#OpenSource**.

## Scopo dello speech

Ci sono moltissime piattaforme che offrono una base **#free** e poi dei piani a pagamento.

Quelle interessanti sono quelle che ti permettono di usare tool come **Ollama** o **LM Studio** (vedi come installarli in questa [guida](../09/README.md)). E perché sarebbero interessanti ? Perché con questi strumenti puoi crearti i tuoi agenti che si basano su ciò che vuoi tu.

## Examples

### Only a specific system prompt

Ammettiamo che ci basta fornire un system prompt specifico per .. pigrizia.

Diamo per scontato che sia già stato installato [Ollama](../09/README.md).

Modifichiamo il [Modelfile](ollama/Modelfile) ed eseguiamo

```sh
ollama create coding -f ollama/Modelfile
```

Proviamo ad installare uno delle possibili estensioni di queste piattaforme, come [Continue DEV](https://www.continue.dev/). E poi configuriamo l'estensione.

Se non vediamo già tra i modelli possibili il nostro **coding**, apriamo il file di configurazione e,

* se non c'è la parte di autodetect di ollama, aggiungiamola

```JSON
    {
      "model": "AUTODETECT",
      "title": "Autodetect",
      "provider": "ollama"
    },
```

* se non basta, aggiungiamo il modello preparato con il `Modelfile`: **coding**

```JSON
    {
      "title": "Coding",
      "model": "coding",
      "provider": "ollama"
    },
```

### More freedom

Ammettiamo di aver bisogno di creare dei comandi come `/dask`, per far rispondere il **#LM** dopo aver consultato la documentazione della libreria Python omonima che abbiamo scaricato.

Diamo per scontato che sia già stato installato [Ollama o LM Studio](../09/README.md).

Useremo FastAPI con Uvicorn per tirare su il nostro sistema di agenti. Per questo motivo, è necessario

* scaricare il repository con l'implementazione base

```sh
git clone https://github.com/bilardi/custom-ai-agents.git
```

* preparare un ambiente Python, per non sporcare il proprio ambiente di default

```sh
cd custom-ai-agents
python -m venv .env
source .env/bin/activate
```

* installare le dipendenze

```sh
cd custom-ai-agents
pip install -r requirements.txt
```

#### Ollama

Di default Ollama parte sulla porta 11434. Se usiamo un'estensione di coding assistants che,

* permette di modificare il default (come [Kilo Code](https://kilocode.ai/)), 
  * sull'estensione metti `http://localhost:11435`
  * su Ollama non devi modificare nulla
  * e puoi eseguire il comando seguente per tirare su il tuo sistema di agenti

```sh
cd custom-ai-agents/fastapi
uvicorn ollama:app --reload --port 11435 # --log-level info
```

* non permette di modificare il default (come [Continue DEV](https://www.continue.dev/))

Su Ollama devi modificare la porta, per esempio, a 11435

```sh
sudo systemctl edit ollama.service

[Service]
Environment="OLLAMA_DEBUG=1"
Environment="OLLAMA_ORIGINS=*"
Environment="OLLAMA_CONTEXT_LENGTH=40000"
Environment="OLLAMA_HOST=0.0.0.0:11435"

sudo systemctl restart ollama.service
```

E devi modificare la porta di Ollama anche sull'applicativo, aggiungendola al comando da eseguire per tirare su il tuo sistema di agenti

```sh
cd custom-ai-agents/fastapi
OLLAMA_PORT=11435 uvicorn ollama:app --reload --port 11434 # --log-level info
```
