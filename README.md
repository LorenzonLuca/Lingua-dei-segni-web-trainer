# Valutatore_Discromatopsia_Web
## Prerequisiti
 - Python
 - Pip
 - venv
 - Node
 - npm
 - MySQL

## Variabili d'ambiente
Per le variabili d'ambiente sono presenti dei file ".env.example" all'interno delle due cartelle frontend e backend. Rimuovere ".example" e inserire dei valori per ogni variabile.

## Avvio App
Come prima cosa bisogna creare il database su cui lavorerà l'applicazione. Basta creare il database vuoto, la struttura verrà creata dall'app.

Per avviare il backend bisogna prima installare le dipendenze all'interno di un virtual environment.

`python -m venv ./venv`

Eseguire

`./venv/Scripts/activate`

`pip install -r requirements.txt`

`python3 app.py` 

Per avviare il frontend invece basta eseguire i seguenti comandi all'interno della cartella frontend.

`npm i`

`npm run dev`

Il sito sarà raggiungibile su "https://localhost:5173"