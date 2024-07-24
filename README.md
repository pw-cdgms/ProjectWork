
**Disclaimer** : Software a solo fine didattico. Non siamo responsabili per qualsiasi uso improprio!

# Project Work 2 (Monitoraggio presenza aziende Online)
### Work In Progress ..
Potrebbe essere quasi tutto pronto.
Ora è possibile utilizzare docker.


## Introduzione
Applicazione Web che permette di inserire il nome di un'azienda locale.
Utilizzo di API per raccogliere online informazioni pubbliche sull'azienda.
Implementazione interfaccia web.


## Struttura del progetto

Abbiamo pensato di organizzare il progetto in container attraverso Docker Compose. Al momento il progetto è chiaramente riassunto nel file `docker-compose.yaml`: abbiamo un container che funge da Server Web, un container di backend che si occupa di fare operazioni di logica, ricerche online e popolare/interagire con i databases. Quindi:


1. Un container che esegue lo script Python (Flask) che funge da server web di backend e distribuisce l'interfaccia web.

2. Un container che agisce come API interna sempre realizzata in python attraverso l'utilizzo di Flask. Questo script si occupa sia di fare le ricerche online (sfruttando API esterne: google etc..), sia di fornire i risultati al server di backend in formato JSON, sia di salvare i risultati delle ricerche in un database.

3. Uno o più container MySql Database(s) in cui verranno salvate sia le informazioni utili al backend sia i risultati delle ricerche esterne.

4. Un container MySql Database in cui vengono salvate le API che l'utente passa alla webapp.

#### TEST FRONTEND:
<p align="center">
<img align="center" src="img/search_page.png" width="900">
</p>

#### TEST RISULTATO DI RICERCA IN JSON (ora aggiungiamo la GUI per i risultati di ricerca e il JSON sarà disponibile solo attraverso CURL/python etc.):

<p align="center">
<img align="center" src="img/json_res.png" width="900">
</p>

#### TEST RISULTATO DI RICERCA IN JSON (con CURL da terminale ancora in fase di TEST):

<p align="center">
<img align="center" src="img/curl_results_terminal.jpg" width="900">
</p>

## Avviare la webapp

Per poter utilizzare la webapp in locale è sufficiente seguire i seguenti passaggi:

#### Come prima cosa creaiamo i secrets per gli utenti di entrambi i database:

```
cd ProjectWork
python setup_secrets.py
```

#### Poi avviamo il progetto docker-compose.yaml:
```
docker-compose up -d
```

Poi nel browser : `https://localhost/`.
<br>
Come prima cosa apparirà un messaggio di ATTENZIONE in giallo:

<p align="center">
<img align="center" src="img/warning.png" width="900">
</p>

Questo perché è necessario fornire alla webapp un file di configurafione in formato JSON così strutturato:

<p align="center">
<img align="center" src="img/config_json_api.png" width="900">
</p>

Sono quindi necessarie 2 API keys di Google con relativi SE_ID, e un'API key di HOSTIO

# TO DO
In questa settimana termineremo il progetto.
La nostra to do list contiene i seguenti punti:
- Frontend (results page) --> ORMAI COMPLETATO.
- Testing/Debugging IMPORTANTE.
- Definire meglio le privacy policy e la conformità con il GDPR
- Presentazione e report.
