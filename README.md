# Corona

## Indice

1. [Introduzione](#1-introduzione)
2. [Struttura Progetto](#2-struttura-progetto)
3. [Requisiti Per Eseguire Il Progetto](#3-requisiti-per-eseguire-il-progetto)
4. [Sviluppi Futuri](#4-sviluppi-futuri)

## 1. Introduzione

Il seguente progetto è stato creato dal seguente gruppo chiamato *Corona-Extra 2.0*:

- Giuseppe Tanzi
- Alessandro Papeo
- Michele Stelluti
- Vincenzo Susso

Il progetto è stato creato per sostenere l'esame di *Ingegneria Della Conoscenza*.

## 2. Struttura Progetto

Il progetto è strutturato nel seguente modo:

```
|–– Cars Project
|    |–– polynomialRegression.py
|    |–– createKB.py
|    |–– useKB.py
|–– data
|    |–– CarPrice.csv
|    |–– knowledgeBase.pl
|–– .gitignore
|-- Documentazione.pdf
|–– README.md
|–– requirements.txt
```

Nel seguito si dettagliano i ruoli dei diversi componenti:

- **Cars Project**: la cartella principale del progetto, in cui è scritto tutto il codice dell’applicazione:
  - **polynomialRegression.py**: file sorgente utilizzato per eseguire le predizioni del prezzo di un automobile;
  - **createKB.py**: file sorgente utilizzato per costruire la *KB* che si trova nel percorso `data/knowledgeBase.pl`;
  - **useKB.py** file sorgente utilizzato per interfacciarsi con la *KB*, in particolar modo questo file utilizza la base di conoscenza che si trova nel percorso `data/knowledgeBase.pl` per rispondere alle domande dell'utente;
- **.gitignore**: file che specifica tutti i file che devono essere esclusi dal sistema di controllo versione;
- **Documentazione.pdf**: documentazione del caso di studio;
- **requirements.txt**: file utilizzato per specificare le librerie necessarie per costruire il `virtual enviroment (venv)` per poter eseguire il progetto.

## 3. Requisiti Per Eseguire Il Progetto

Per eseguire il progetto è necessario installare i seguenti programmi:

- `Python 3.9.1`
- `SWI-Prolog 8.2.4`

Una volta scaricato il progetto dal sistema di controllo versione, per poterlo eseguire è necessario aprire il `terminale`, spostarsi sulla `cartella del progetto` e digitare i seguenti comandi:

- `$ python -m venv venv`
- `$ venv\Scripts\activate`
- `$ pip install -r requirements.txt`

## 4. Sviluppi Futuri

In futuro, il progetto da noi sviluppato potrà essere utilizzato in larga scala da più aziende automobilistiche per la predizione dei prezzi di vendita in diversi mercati del mondo, ma anche in diversi contesti d'uso: un esempio consiste nel riaddattare il software per la stima di prezzi di auto usate. Per far ciò sarà necessario utilizzare un dataset.
Per quanto riguarda la base di conoscenza, ciò che è stato inserito nel nostro progetto, è una piccola demo a dimostrazione delle grandi potenzialità che lo strumento implementato può offrire: ad oggi è utilizzato per visualizzare informazioni sulle auto ma in uno sviluppo futuro potrebbe essere utilizzato per la diagnostica di malfunzionamenti delle auto usate che potrebbe, quindi, influenzare il costo di vendita.
