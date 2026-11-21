# Li Fòli – Casale di Campagna

Balaiana, Luogosanto (SS) · Gallura, Sardegna

## Struttura
- **`docs/`** – sito web (italiano, inglese, spagnolo, tedesco), pubblicato con GitHub Pages.
  - I testi si modificano in `docs/src/build.py`, il layout in `docs/src/template.html`.
  - Dopo una modifica: `python3 docs/src/build.py` rigenera tutte le lingue.
- **`gestionale/`** – gestionale interno (prenotazioni, contabilità, scadenze, documenti, ruoli).
  Lo stesso `Index.html` funziona in tre modi:
  - pubblicato su Claude: dati condivisi online tra i soci (modalità in uso);
  - su Google Apps Script con `Code.gs`: dati in un Google Sheet (vedi `gestionale/ISTRUZIONI.md`);
  - aperto da solo nel browser: demo con dati di esempio.
  I dati reali non stanno mai in questo repository.
