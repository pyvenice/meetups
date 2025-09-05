# PyVenice #0 - #VibeCoding #Workshop

Ospitati dall'[ESC](https://endsummer.camp/), [Marco Gaion](https://www.linkedin.com/in/marco-gaion/) e [Davide Eynard](https://www.linkedin.com/in/deynard/) hanno proposto 3 speech sulla **#GenerativeAI** conclusisi con un **#lab** che ha visto il supporto dello staff di PyVenice.

Link del primo [meetup](https://www.meetup.com/pyvenice/events/310450900/) di PyVenice, [agenda](https://pretalx.endsummer.camp/2K25/talk/) dell'ESC.

## Scopo del lab

Arrivare ad una consapevolezza degli strumenti **#OpenSource** che possono risultare utili per il **#VibeCoding**:

* usare un modello di Language Model (LM) in locale
* usare un agente AI in locale
* usare un IDE con i propri modelli e i propri agenti

Per chi comincia da zero, probabile che questo sia l'inizio di un percorso e che non si tocchino tutti i punti. Ma è a disposizione un canale discord per approfondire e fare domande: la community risponderà. Se non hai il link al canale discord, contattaci su [telegram](https://venice.python.it).

## __init__ phase

### Gestione dei modelli in locale

Il materiale di partenza può essere differente, a seconda della vostra attitudine:

* se preferite la CLI, probabilmente preferirete usare [ollama](https://ollama.com/download)
* se preferite la GUI, un'interfaccia web, meglio [LM Studio](https://lmstudio.ai/download)

#### Ollama

Alcuni tips & tricks importanti:

* Ollama è ancora distribuito ufficialmente come open source, anche se i client desktop non lo sono
* ci sono alcune variabili d'ambiente che conviene configurare per abilitare
  * i log, se si vuole fare debugging
  * il Cross-Origin Resource Sharing (CORS), che è un sistema di permessi tra siti web gestito dai browser per evitare accessi non autorizzati
    * le API di Ollama gireranno in locale su di una determinata porta
    * le richieste a quelle API gireranno in locale, ma su una porta differente: questo per il browser vuol dire un sito differente e se non si attivano le regole CORS, la richiesta sarà bloccata
  * il contesto più lungo, il deafult è 4096 token, che più o meno vuol dire 4096 parole
    * il default va bene finché si fanno domande semplici al modello
    * ma quando si comincia a fare richieste con un contesto che conta file locali, richieste agli agenti, storico della sessione di una chat, .., cominciano ad essere pochi 4096 token 

E' possibile configurarle allo start del servizio

```sh
OLLAMA_DEBUG=1 OLLAMA_ORIGINS="*" OLLAMA_CONTEXT_LENGTH=40000 ollama serve
```

Oppure si possono impostare le variabili d'ambiente in modo persistente

```sh
# macOS
launchctl setenv OLLAMA_DEBUG 1
launchctl setenv OLLAMA_ORIGINS "*"
launchctl setenv OLLAMA_CONTEXT_LENGTH 40000

# linux
sudo systemctl edit ollama.service

[Service]
Environment="OLLAMA_DEBUG=1"
Environment="OLLAMA_ORIGINS=*"
Environment="OLLAMA_CONTEXT_LENGTH=40000"

# docker
docker run -d -p 11434:11434 \
  -e OLLAMA_DEBUG=1 \
  -e OLLAMA_ORIGINS="*" \
  -e OLLAMA_CONTEXT_LENGTH=40000 \
  ollama/ollama

# docker-compose
cat docker-compose.yaml
services:
  ollama:
    image: ollama/ollama:latest
    environment:
      - OLLAMA_DEBUG=1
      - OLLAMA_ORIGINS=*
      - OLLAMA_CONTEXT_LENGTH=40000
```

Per Windows,

* chiudi Ollama (dalla tray/app)
* apri Pannello di Controllo → Variabili d'ambiente (o usa le Impostazioni su Windows 11)
* crea o modifica:
  * Nome: OLLAMA_DEBUG
  * Valore: 1
  * così anche per
    * OLLAMA_ORIGINS=*
    * OLLAMA_CONTEXT_LENGTH=40000
* salva e riavvia Ollama

#### LM Studio

Alcuni tips & tricks importanti:

* LM Studio ha diverso codice open source (per CLI, SDK e MLX) ma ha una licenza proprietaria per il componente GUI, cioè l'interfaccia desktop:
  * Element Labs concede all’utente una licenza non esclusiva, non trasferibile, valida solo per uso personale o interno aziendale e in accordo con la documentazione
  * L’uso commerciale è ammesso senza costi aggiuntivi, ma va fatto secondo le regole indicate e senza redistribuire o modificare il software
* per abilitare CORS, è necessario installare su Firefox [CORS Everywhere](https://addons.mozilla.org/en-US/firefox/addon/cors-everywhere/) o su Chrome [Cross Domain - CORS](https://chromewebstore.google.com/detail/cross-domain-cors/mjhpgnbimicffchbodmgfnemoghjakai) ([dettagli](https://github.com/mozilla-ai/wasm-agents-blueprint?tab=readme-ov-file#troubleshooting))

### Modelli che potreste scaricare in locale

Quando saremo all'ESC avremo il wifi, ma non potremo metterci tutti a scaricare in quel momento:

* sarà messo a disposizione un server dove sono installati una serie di modelli (dettagli su discord, durante il **#lab**)
* se vuoi installare nel tuo locale, ricordati di scaricare quelli che potrai usare, in base alle risorse che disponi:
  * almeno 16GB di RAM
    * [qwen3:8b](https://ollama.com/library/qwen3:8b)
    * [deepseek-r1:latest](https://ollama.com/library/deepseek-r1:latest)
  * almeno 64GB di RAM
    * [gpt-oss:latest](https://ollama.com/library/gpt-oss:latest)

In realtà, **esistono modelli che possono funzionare anche con 8GB di RAM**, come [qwen3:4b](https://ollama.com/library/qwen3:4b) per sperimentare tutto il percorso in locale.

```sh
# model download, pull example
ollama pull qwen3
```

## Exercises

### by CLI

Per Ollama è possibile usare la CLI e fare domande direttamente ai modelli tramite la console che verrà aperta dopo il seguente comando:

```sh
ollama run qwen3
>>> Chi ha scritto I promessi sposi?
Alessandro Manzoni
```

Oppure invocare le sue API:

```sh
curl http://localhost:11434/api/generate -d '{
  "model": "qwen3",
  "prompt": "Chi ha scritto I promessi sposi?",
  "stream": false
}'
{"model":"qwen3","created_at":"2025-09-02T10:00:00.000000001Z","response":"Alessandro Manzoni","done":true, ..}
```

```sh
curl http://localhost:11434/api/chat -d '{
  "model": "qwen3",
  "messages": [
    {"role": "system", "content": "Sei un assistente di un docente universitario."},
    {"role": "user", "content": "Spiegami come funzionano le API di Ollama in breve."}
  ],
  "stream": false
}'
{"model":"qwen2.5","created_at":"2025-09-05T14:18:57.735523384Z","message":{"role":"assistant","content":"Le API di Ollama sono strumenti software che consentono l'integrazione e l'interazione tra vari servizi digitali o applicazioni. Specificamente, Ollama offre API per diverse funzionalità, come la generazione di testi, la traduzione, la ricerca su dati e altro ancora.\n\nIn pratica, un utente può inviare richieste attraverso queste API in formato JSON o altri formati di codifica standard. .."}
```

### by Python

Consigliamo di preparare un ambiente dedicato (per non "sporcare" il tuo sistema),

```sh
# environment 
mkdir workshop
cd workshop
python -m venv .venv
source .venv/bin/activate
```

#### Ollama

Lo stesso esempio di Ollama by CLI fatto con Python,

```sh
# project download
git clone https://github.com/pyvenice/meetups
cd meetups
pip install -r requirements.txt

# run script
cd meetups/2025/09
python ollama.python.py
```

#### Agents AI

Il codice degli esempi che andremo a vedere sono scaricabili da [GitHub](https://github.com/aittalam/esc2025_agents_workshop) e sono basati su [any-agent](https://github.com/mozilla-ai/any-agent).

### OpenAI simulation

#### Ollama

Potrebbe bastare impostare le variabili d'ambiente

```sh
export OPENAI_API_BASE=http://localhost:11434/v1
export OPENAI_API_KEY=ollama
```

Poi da script Python le usi,

```sh
# run script
cd meetups/2025/09
python ollama.openai.py
```

### by GUI

#### LM Studio

Con LM Studio è possibile,

* gestire i modelli scaricabili in locale
* interagire con i modelli stile ChatGPT
* caricare documenti e dialogare con il modello

E lato sviluppatori,

* offre localmente un endpoint compatibile con l'API OpenAI
* ha un SDK in Python e TypeScript per chat e agenti
* supporta i server MCP (Model Context Protocol) per applicazioni esterne e il richiamo di funzioni/tool esterni

Quindi, facendo partire il file scaricato dalla pagina di [download](https://lmstudio.ai/download) nel seguente modo,

```sh
chmod +x LM-Studio-*.AppImage
./LM-Studio-*.AppImage
```

Usiamo la versione "Power user" e skippa in alto a destra.

* dall'iconcina viola, possiamo scaricare un modello
* dall'iconcina rossa, possiamo gestire i modelli
  * dall'iconcina della configurazione del modello, è possibile modificare alcuni parametri
    * Context length
* dall'iconcina verde, possiamo gestire le API
  * bisogna verificare che lo Status del server sia Running
  * su Settings abilitare CORS
  * selezionare un modello di riferimento

#### WebAssembly (Wasm)

Per chi non sviluppa, è possibile sfruttare un'interfaccia web apposita che si chiama [Wasm-agents](https://github.com/aittalam/wasm-agents-blueprint/tree/esc2025): è possibile scaricare direttamente una [versione che punta al server](https://github.com/aittalam/wasm-agents-blueprint/tree/esc2025/demos) che sarà messo a disposizione durante il **#lab**.

Se non usi il client git, usa direttamente lo [zip](https://github.com/aittalam/wasm-agents-blueprint/archive/refs/heads/esc2025.zip) oppure via git:

```sh
# project download
git clone https://github.com/aittalam/wasm-agents-blueprint
cd wasm-agents-blueprint/demos
git fetch origin esc2025
git checkout esc2025
pwd
~/github/bilardi/pyvenice.meetups/2025/09/workshop/wasm-agents-blueprint/demos
# on browser
file:///home/bilardi/github/bilardi/pyvenice.meetups/2025/09/workshop/wasm-agents-blueprint/demos
```

Gli script che possiamo usare sono:

* local_model.html
  * conta dei caratteri in una stringa
  * visita una pagina web
* local_mcpd.html
  * in **Available Tools** ci sono gli agenti che si possono richiamare

Domande da provare:

* What are the novels by Cory Doctorow, sorted by date ? Search on zim
* Quali sono i romanzi di Cory Doctorow, ordinati per data ? Cerca su zim.

#### IDE

Per chi sviluppa, è possibile installare un'estensione come [Continue](https://www.continue.dev/) per sfruttare:

* i modelli installati localmente con Ollama o LM Studio 
* gli agenti preparati con Python
