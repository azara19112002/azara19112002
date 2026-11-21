# Li Fòli – Gestionale: installazione (circa 10 minuti)

Il gestionale gira su Google Apps Script. I dati restano nel vostro Google Drive,
in un Google Sheet chiamato "Li Fòli – Dati gestionale"; gli allegati (fatture, SCIA,
contratti…) vanno nella cartella "Li Fòli – Gestionale/Allegati".

## 1. Crea il progetto
1. Entra su https://script.google.com con l'account che deve essere **proprietario** dei dati
   (es. lifolicampagna@gmail.com) e clicca **Nuovo progetto**.
2. Rinominalo "Li Fòli Gestionale" (in alto a sinistra).
3. Nel file `Codice.gs` cancella tutto e incolla il contenuto di **Code.gs**.
4. Clicca **+** accanto a "File" → **HTML**, chiamalo esattamente `Index` e incolla il contenuto di **Index.html**.
5. Vai su **Impostazioni progetto** (ingranaggio) → spunta "Mostra il file manifest appsscript.json".
   Torna all'editor, apri `appsscript.json` e sostituiscilo con il contenuto di **appsscript.json**.
6. Salva (Ctrl+S).

## 2. Installa
1. Nella barra in alto scegli la funzione **setup** e clicca **Esegui**.
2. Google chiederà le autorizzazioni (Drive, Fogli, email): clicca "Consenti".
   Se compare "App non verificata" → *Avanzate* → *Vai a Li Fòli Gestionale*. È normale: l'app è vostra.
3. `setup` crea il foglio dati, la cartella allegati, ti registra come **admin** e attiva
   l'email di promemoria ogni mattina alle 8.

## 3. Pubblica la web app
1. **Distribuisci** → **Nuova distribuzione** → tipo **App web**.
2. *Esegui come*: **Utente che accede all'app web**.
3. *Chi ha accesso*: **Chiunque abbia un account Google** (l'accesso vero è controllato dalla lista Utenti del gestionale: chi non è in lista vede "non abilitato").
4. **Distribuisci** e copia l'URL che finisce con `/exec`. Quello è l'indirizzo del gestionale.

## 4. Aggiungi tuo fratello
Apri il gestionale → **Utenti e ruoli** → **+ Nuovo utente** → email Google di tuo fratello, ruolo **socio** (o admin).
Il foglio dati e la cartella vengono condivisi automaticamente con lui.

Ruoli disponibili:
- **admin** – tutto, compresa la gestione utenti
- **socio** – tutto tranne la gestione utenti
- **collaboratore** – vede prenotazioni e camere, gestisce le pulizie (per chi fa le pulizie)
- **contabile** – sola lettura di contabilità, fatture, scadenze, documenti (per il commercialista)

## 5. Collegalo al dominio (gestionale.lifolicasaledicampagna.it)
Google non permette di mettere un dominio proprio direttamente su una web app Apps Script. Due strade:
- **Reindirizzamento (più semplice)**: nel pannello del registrar del dominio crea il sottodominio
  `gestionale` con un *redirect/inoltro web* verso l'URL `/exec`. Digitando gestionale.lifolicasaledicampagna.it
  si arriva al gestionale (poi la barra mostra l'indirizzo Google).
- **Google Sites**: crea un sito Google, incorpora l'URL `/exec` a tutta pagina e collega il sito
  al sottodominio da *Impostazioni → Domini personalizzati*.

## Aggiornamenti futuri
Quando cambi il codice: **Distribuisci → Gestisci distribuzioni → ✏️ → Versione: Nuova versione → Distribuisci**.
L'URL resta lo stesso.

## Note
- Tutte le modifiche vengono registrate in **Registro attività** (chi, cosa, quando).
- In **Scadenze** il pulsante "Aggiungi scadenze tipiche" inserisce i principali adempimenti di una S.r.l.s.
  ricettiva: **le date sono indicative e vanno verificate con il commercialista**.
- Il "Bilancio e report" calcola il risultato per cassa dai movimenti inseriti: è uno strumento di
  controllo, non sostituisce il bilancio ufficiale.
- Backup: il Google Sheet si può scaricare in qualsiasi momento (File → Scarica → Excel).
