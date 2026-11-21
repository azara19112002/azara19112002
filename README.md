# Li Fòli – Casale di Campagna

Balaiana, Luogosanto (SS) · Gallura, Sardegna

## Struttura
- **`docs/`** – sito web (italiano, inglese, spagnolo, tedesco), pubblicato con GitHub Pages.
  - I testi si modificano in `docs/src/build.py`, il layout in `docs/src/template.html`.
  - Dopo una modifica: `python3 docs/src/build.py` rigenera tutte le lingue.
- **`gestionale/`** – gestionale interno su Google Apps Script (prenotazioni, contabilità,
  scadenze, documenti, ruoli). Installazione: vedi `gestionale/ISTRUZIONI.md`.
